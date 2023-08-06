import re
import sys
import uuid

import tomlkit


# disable warnings if they are not explicitly wanted
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore')

import json
import math
import logging
from datetime import datetime
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path

import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from psutil import cpu_count

from slrkit_utils.argument_parser import ArgParse
from utils import substring_index, STOPWORD_PLACEHOLDER, assert_column
from join_lda_info import join_lda_info

PHYSICAL_CPUS = cpu_count(logical=False)
MIN_ALPHA_VAL = 1e-20


def to_ignore(_):
    return ['lda*.json', 'lda_info*.txt']


def init_argparser():
    """
    Initialize the command line parser.

    :return: the command line parser
    :rtype: ArgParse
    """
    epilog = "This script outputs the topics in " \
             "<outdir>/lda_terms-topics_<date>_<time>.json and the topics" \
             "assigned to each document in" \
             "<outdir>/lda_docs-topics_<date>_<time>.json"
    parser = ArgParse(description='Performs the LDA on a dataset', epilog=epilog)
    parser.add_argument('preproc_file', action='store', type=Path,
                        help='path to the the preprocess file with the text to '
                             'elaborate.', input=True)
    parser.add_argument('terms_file', action='store', type=Path,
                        help='path to the file with the classified terms.',
                        input=True)
    parser.add_argument('outdir', action='store', type=Path, nargs='?',
                        default=Path.cwd(), help='path to the directory where '
                                                 'to save the results.')
    parser.add_argument('--text-column', '-t', action='store', type=str,
                        default='abstract_lem', dest='target_column',
                        help='Column in preproc_file to process. '
                             'If omitted %(default)r is used.')
    parser.add_argument('--title-column', action='store', type=str,
                        default='title', dest='title',
                        help='Column in preproc_file to use as document title. '
                             'If omitted %(default)r is used.')
    parser.add_argument('--topics', action='store', type=int,
                        default=20, help='Number of topics. If omitted '
                                         '%(default)s is used')
    parser.add_argument('--alpha', action='store', type=str,
                        default='auto', help='alpha parameter of LDA. If '
                                             'omitted %(default)s is used. '
                                             'Cannot be less than '
                                             '{}'.format(MIN_ALPHA_VAL))
    parser.add_argument('--beta', action='store', type=str,
                        default='auto', help='beta parameter of LDA. If omitted'
                                             ' %(default)s is used')
    parser.add_argument('--no_below', action='store', type=int,
                        default=20, help='Keep tokens which are contained in at'
                                         ' least this number of documents. If '
                                         'omitted %(default)s is used')
    parser.add_argument('--no_above', action='store', type=float,
                        default=0.5, help='Keep tokens which are contained in '
                                          'no more than this fraction of '
                                          'documents (fraction of total corpus '
                                          'size, not an absolute number). If '
                                          'omitted %(default)s is used')
    parser.add_argument('--seed', type=int, default=123,
                        help='Seed to be used in training. Default %(default)r')
    parser.add_argument('--model', action='store_true',
                        help='if set, the lda model is saved to directory '
                             '<outdir>/lda_model. The model is saved '
                             'with name "model.')
    parser.add_argument('--no-relevant', action='store_true',
                        help='if set, use only the term labelled as keyword')
    parser.add_argument('--load-model', action='store',
                        help='Path to a directory where a previously trained '
                             'model is saved. Inside this directory the model '
                             'named "model" is searched. the loaded model is '
                             'used with the dataset file to generate the topics'
                             ' and the topic document association')
    parser.add_argument('--no_timestamp', action='store_true',
                        help='if set, no timestamp is added to the topics file '
                             'names')
    parser.add_argument('--placeholder', '-p',
                        default=STOPWORD_PLACEHOLDER,
                        help='Placeholder for barrier word. Also used as a '
                             'prefix for the relevant words. '
                             'Default: %(default)s')
    parser.add_argument('--delimiter', action='store', type=str,
                        default='\t', help='Delimiter used in preproc_file. '
                                           'Default %(default)r')
    parser.add_argument('--config', '-c', action='store', type=Path,
                        help='Path to a toml config file like the one used by '
                             'the slrkit lda command. It overrides all the cli '
                             'arguments.', cli_only=True)
    return parser


def load_term_data(terms_file):
    words_dataset = pd.read_csv(terms_file, delimiter='\t',
                                encoding='utf-8')
    try:
        terms = words_dataset['term'].to_list()
    except KeyError:
        terms = words_dataset['keyword'].to_list()
    term_labels = words_dataset['label'].to_list()
    return term_labels, terms


def load_ngrams(terms_file, labels=('keyword', 'relevant')):
    term_labels, terms = load_term_data(terms_file)
    zipped = zip(terms, term_labels)
    good = [x[0] for x in zipped if x[1] in labels]
    ngrams = {1: set()}
    for x in good:
        n = x.count(' ') + 1
        try:
            ngrams[n].add(x)
        except KeyError:
            ngrams[n] = {x}

    return ngrams


def check_ngram(doc, idx):
    for dd in doc:
        r = range(dd[0][0], dd[0][1])
        yield idx[0] in r or idx[1] in r


def filter_doc(d: str, ngram_len, terms, placeholder, relevant_prefix):
    additional = []
    end = False
    idx = 0
    d = re.sub(rf'\B{placeholder}\B', ' ', d)
    while not end:
        i = d.find(relevant_prefix, idx)
        if i < 0:
            end = True
        else:
            stop = d.find(relevant_prefix, i+1)
            if stop > 0:
                additional.append(((i+1, stop), d[i+1:stop]))
                idx = stop + 1
            else:
                end = True

    doc = []
    flag = False
    for n in ngram_len:
        for t in terms[n]:
            for idx in substring_index(d, t):
                if flag and any(check_ngram(doc, idx)):
                    continue

                doc.append((idx, t.replace(' ', '_')))

        flag = True

    doc.extend(additional)
    doc.sort(key=lambda dd: dd[0])
    return [t[1] for t in doc]


def load_terms(terms_file, labels=('keyword', 'relevant')):
    term_labels, terms = load_term_data(terms_file)
    zipped = zip(terms, term_labels)
    good = [x for x in zipped if x[1] in labels]
    good_set = set()
    for x in good:
        good_set.add(x[0])

    return good_set


def save_filtered_column(preproc_file, filtered_list, optional_filtered_col,
                         delimiter='\t'):
    try:
        dataset = pd.read_csv(preproc_file,
                              delimiter=delimiter,
                              encoding='utf-8')
    except FileNotFoundError as err:
        msg = 'Error: file {!r} not found'
        sys.exit(msg.format(err.filename))
    joined = []
    for elem in filtered_list:
        joined.append(' '.join(elem))
    dataset[optional_filtered_col] = joined
    dataset.to_csv(preproc_file, sep=delimiter, index_label='id')


def linear_filtering(documents, ngram_len, terms, placeholder, relevant_prefix):
    logger = logging.getLogger('debug_logger')
    docs = []
    for i, d in enumerate(documents):
        result = filter_doc(d, ngram_len, terms, placeholder, relevant_prefix)
        docs.append(result)
        logger.debug(f'Completed document: {i}/{len(documents)}')
    return docs


def parallel_filtering(documents, ngram_len, terms, placeholder, relevant_prefix):
    with Pool(processes=PHYSICAL_CPUS) as pool:
        docs = pool.starmap(filter_doc,
                            zip(documents,
                                repeat(ngram_len),
                                repeat(terms),
                                repeat(placeholder),
                                repeat(relevant_prefix)))
    return docs


def generate_filtered_docs_ngrams(terms_file, preproc_file,
                                  target_col='abstract_lem', title_col='title',
                                  optional_filtered_col='abstract_filtered',
                                  delimiter='\t',
                                  labels=('keyword', 'relevant'),
                                  placeholder=STOPWORD_PLACEHOLDER,
                                  relevant_prefix=STOPWORD_PLACEHOLDER):
    logger = logging.getLogger('debug_logger')
    terms = load_ngrams(terms_file, labels)
    ngram_len = sorted(terms, reverse=True)
    src_docs, titles, filtered_docs = load_documents(preproc_file,
                                                     target_col,
                                                     title_col,
                                                     optional_filtered_col,
                                                     delimiter)
    # TODO: the logic should be improved to regenerate the filtered text
    # if the terms file is newer that the preproc file; otherwise this
    # would require the user to manually delete the column from the
    # preproc file to trigger the regeneration of the filtered text
    # MAYBE this could be made interactive, or at least an alert
    # could be printed and an option to force the re-generation
    # could be provided
    if filtered_docs is not None:
        docs = filtered_docs
        msg = (
            f"Using data from column "
            f"'{optional_filtered_col}' in {preproc_file}"
        )
        print(msg)
        logger.debug(msg)
    else:
        msg = f"Filtering data from '{target_col}' in {preproc_file}"
        print(msg)
        logger.debug(msg)
        docs = linear_filtering(src_docs, ngram_len, terms, placeholder, relevant_prefix)
        # docs = parallel_filtering(src_docs, ngram_len, terms, placeholder, relevant_prefix)
        msg = (
            f"Saving filtered data in column "
            f"'{optional_filtered_col}' of {preproc_file}"
        )
        print(msg)
        logger.debug(msg)
        save_filtered_column(preproc_file, docs, optional_filtered_col,
                             delimiter=delimiter)
    return docs, titles


def load_additional_terms(input_file):
    """
    Loads a list of keyword terms from a file

    This functions skips all the lines that starts with a '#'.
    Each term is split in a tuple of strings

    :param input_file: file to read
    :type input_file: str
    :return: the loaded terms as a set of strings
    :rtype: set[str]
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        rel_words_list = f.read().splitlines()

    rel_words_list = {w.replace(' ', '_')
                      for w in rel_words_list
                      if w != '' and w[0] != '#'}
    return rel_words_list


def prepare_documents(preproc_file, terms_file, labels,
                      target_col='abstract_lem', title_col='title',
                      delimiter='\t', placeholder=STOPWORD_PLACEHOLDER,
                      relevant_prefix=STOPWORD_PLACEHOLDER):
    """
    Elaborates the documents preparing the bag of word representation

    :param preproc_file: path to the csv file with the lemmatized abstracts
    :type preproc_file: str or Path
    :param terms_file: path to the csv file with the classified terms
    :type terms_file: str or Path
    :param target_col: name of the column in preproc_file with the document text
    :type target_col: str
    :param title_col: name of the column used as document title
    :type title_col: str
    :param delimiter: delimiter used in preproc_file
    :type delimiter: str
    :param labels: use only the terms classified with the labels specified here
    :type labels: tuple[str]
    :param placeholder: placeholder for stop-words
    :type placeholder: str
    :param relevant_prefix: prefix used to mark relevant terms
    :type relevant_prefix: str
    :return: the documents as bag of words and the document titles
    :rtype: tuple[list[list[str]], list[str]]
    """
    ret = generate_filtered_docs_ngrams(terms_file, preproc_file,
                                        target_col=target_col,
                                        title_col=title_col,
                                        delimiter=delimiter,
                                        labels=labels,
                                        placeholder=placeholder,
                                        relevant_prefix=relevant_prefix)
    docs, titles = ret
    return docs, titles


def prepare_corpus(docs, no_above, no_below):
    """
    Prepares the bag-of-words representation of the documents

    It prepares also the dictionary object used by LdaModel
    :param docs: documents to elaborate
    :type docs: list[list[str]]
    :param no_above: keep terms which are contained in no more than this
        fraction of documents (fraction of total corpus size, not an absolute
        number).
    :type no_above: float
    :param no_below: keep tokens which are contained in at least this number of
        documents (absolute number).
    :type no_below: int
    :return: bag-of-words representation of the documents and the dictionary object.
        If all the documents are empty after the filtering phase, the returned
        values are both None.
    :rtype: tuple[list[list[tuple[int, int]]] or None, Dictionary or None]
    """
    # Make a index to word dictionary.
    dictionary = Dictionary(docs)
    # Filter out words that occur less than no_above documents, or more than
    # no_below % of the documents.
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)
    # Finally, we transform the documents to a vectorized form. We simply
    # compute the frequency of each word, including the bigrams.
    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    try:
        _ = dictionary[0]  # This is only to "load" the dictionary.
    except KeyError:
        # nothing in this corpus
        return None, None
    else:
        return corpus, dictionary


def train_lda_model(docs, topics=20, alpha='auto', beta='auto', no_above=0.5,
                    no_below=20, seed=None):
    """
    Trains the lda model

    Each parameter has the default value used also as default by the lda.py script
    :param docs: documents train the model upon
    :type docs: list[list[str]]
    :param topics: number of topics
    :type topics: int
    :param alpha: alpha parameter
    :type alpha: float or str
    :param beta: beta parameter
    :type beta: float or str
    :param no_above: keep terms which are contained in no more than this
        fraction of documents (fraction of total corpus size, not an absolute
        number).
    :type no_above: float
    :param no_below: keep tokens which are contained in at least this number of
        documents (absolute number).
    :type no_below: int
    :param seed: seed used for random generator
    :type seed: int or None
    :return: the trained model and the dictionary object used in training
    :rtype: tuple[LdaModel, Dictionary]
    """
    corpus, dictionary = prepare_corpus(docs, no_above, no_below)
    if corpus is None:
        sys.exit('All filtered documents are empty. Check the filter parameters '
                 'and the input files.')
    id2word = dictionary.id2token
    # filter the empty documents
    bows = [c for c in corpus if c != []]
    # Train LDA model.
    try:
        model = LdaModel(
            corpus=bows,
            id2word=id2word,
            chunksize=len(corpus),
            alpha=alpha,
            eta=beta,
            num_topics=topics,
            random_state=seed,
            minimum_probability=0.0
        )
    except ValueError as err:
        if 'alpha' in err.args[0]:
            msg = 'Invalid value {!r} for parameter alpha'.format(alpha)
        elif 'eta' in err.args[0]:
            msg = 'Invalid value {!r} for parameter beta'.format(beta)
        else:
            raise
        sys.exit(msg)
    return model, dictionary


def prepare_topics(model, docs, titles, dictionary):
    """
    Prepare the dicts for the topics and the document topic assignment

    :param model: the trained lda model
    :type model: LdaModel
    :param docs: the documents to evaluate to assign the topics
    :type docs: list[list[str]]
    :param titles: the titles of the documents
    :type titles: list[str]
    :param dictionary: the gensim dictionary object used for training
    :type dictionary: Dictionary
    :return: the dict of the topics, the docs-topics assignement and
        the average coherence score
    :rtype: tuple[dict[int, dict[str, str or dict[str, float]]],
        list[dict[str, int or bool or str or dict[int, str]]], float]
    """
    docs_topics = []
    not_empty_docs = []
    topics_n_digit = math.floor(math.log10(model.num_topics) + 1)
    for i, (title, d) in enumerate(zip(titles, docs)):
        bow = dictionary.doc2bow(d)
        isempty = False
        if bow:
            t = model.get_document_topics(bow)
            t.sort(key=lambda x: x[1], reverse=True)
            not_empty_docs.append(d)
        else:
            # document is empty after the filtering so no topics
            t = []
            isempty = True
        d_t = {
            'id': i,
            'title': title,
            'topics': {f'{tu[0]:0{topics_n_digit}d}': float(tu[1]) for tu in t},
            'empty': isempty
        }
        docs_topics.append(d_t)

    cm = CoherenceModel(model=model, texts=not_empty_docs,
                        dictionary=dictionary,
                        coherence='c_v', processes=1)  # PHYSICAL_CPUS)

    # Average topic coherence is the sum of topic coherences of all topics,
    # divided by the number of topics.
    avg_topic_coherence = cm.get_coherence()
    coherence = cm.get_coherence_per_topic()
    topics = {}
    topics_order = list(range(model.num_topics))
    topics_order.sort(key=lambda x: coherence[x], reverse=True)
    for i in topics_order:
        topic = model.show_topic(i)
        num = f'{i:0{topics_n_digit}d}'
        t_dict = {
            'name': f'Topic {num}',
            'terms_probability': {t[0]: float(t[1]) for t in topic},
            'coherence': f'{float(coherence[i]):.5f}',
        }
        topics[num] = t_dict

    return topics, docs_topics, avg_topic_coherence


def load_documents(preproc_file, target_col, title_col, optional_filtered_col,
                   delimiter):
    try:
        dataset = pd.read_csv(preproc_file,
                              delimiter=delimiter,
                              encoding='utf-8')
    except FileNotFoundError as err:
        msg = 'Error: file {!r} not found'
        sys.exit(msg.format(err.filename))

    assert_column(str(preproc_file), dataset, [target_col, title_col])
    dataset.fillna('', inplace=True)
    titles = dataset[title_col].to_list()
    documents = dataset[target_col].to_list()
    # processes the optional_filtered_col if present
    if optional_filtered_col in dataset:
        filtered_list = dataset[optional_filtered_col].to_list()
        filtered_split = []
        for s in filtered_list:
            s_split = s.split(' ')
            filtered_split.append(s_split)
    else:
        filtered_split = None
    return documents, titles, filtered_split


def output_topics(topics, docs_topics, outdir, file_prefix, uid,
                  use_timestamp=True):
    """
    Saves the topics and docs-topics association to json files

    The saved files are: <outdir>/<file_prefix>_terms-topics_<timestamp>.json
    for the topics, and <outdir>/<file_prefix>_docs-topics_<timestamp>.json for
    the docs-topics association.
    Also outputs the file <outdir>/<file_prefix>_info_<timestamp>.txt with all
    the information about topics and documents joined in a single file.
    This file is in the format produced by the join_lda_info.py.
    :param topics: dict of the topics as returned by prepare_topics
    :type topics: dict[int, dict[str, str or dict[str, float]]]
    :param docs_topics: docs-topics association as returned by prepare_topics
    :type docs_topics: list[dict[str, int or bool or str or dict[int, str]]]
    :param outdir: where to save the files
    :type outdir: Path
    :param file_prefix: prefix of the files
    :type file_prefix: str
    :param uid: uuid associated to the generated topics
    :type uid: str
    :param use_timestamp: if True (the default) add a timestamp to file names
    :type use_timestamp: bool
    """
    if use_timestamp:
        now = datetime.now()
        timestamp = f'{now:_%Y-%m-%d_%H%M%S}'
    else:
        timestamp = ''
    name = f'{file_prefix}_terms-topics{timestamp}_{uid}.json'
    topic_file = outdir / name
    with open(topic_file, 'w') as file:
        json.dump(topics, file, indent='\t')

    name = f'{file_prefix}_docs-topics{timestamp}_{uid}.json'
    docs_file = outdir / name
    with open(docs_file, 'w') as file:
        json.dump(docs_topics, file, indent='\t')

    info_file = outdir / f'{file_prefix}_info{timestamp}_{uid}.txt'
    join_lda_info(topics, docs_topics, str(info_file))


def save_toml_files(args, results_df, result_dir):
    """
    Saves the toml files that will be used to load the models in lda.py

    The toml file are saved in <outdir>/toml. If this directory not exists, it
    is created.
    :param args: cli arguments.
        Must have preproc_file, terms_file, outdir as Path. target_colum, title,
        placeholder, delimiter as str. The meaning of these attributes is the
        same as the one defined in the init_argparser in this file
    :type args: argparse.Namespace
    :param results_df: dataframe with the training results
    :type results_df: pd.DataFrame
    :param result_dir: path to the directory of the results
    :type result_dir: Path
    """
    toml_dir = result_dir / 'toml'
    toml_dir.mkdir(exist_ok=True)
    for _, row in results_df.iterrows():
        conf = tomlkit.document()
        conf.add('preproc_file', str(args.preproc_file))
        conf.add('terms_file', str(args.terms_file))
        conf.add('outdir', str(args.outdir))
        conf.add('text-column', args.target_column)
        conf.add('title-column', args.title)
        conf.add('topics', row['topics'])
        conf.add('alpha', row['alpha'])
        conf.add('beta', row['beta'])
        conf.add('no_below', row['no_below'])
        conf.add('no_above', row['no_above'])
        if row['seed'] is None:
            conf.add('seed', '')
        else:
            conf.add('seed', row['seed'])
        conf.add('model', False)
        conf.add('no-relevant', False)
        u = row['uuid']
        conf.add('load-model', str(result_dir / 'models' / u))
        conf.add('placeholder', args.placeholder)
        conf.add('delimiter', args.delimiter)
        with open(toml_dir / ''.join([u, '.toml']), 'w') as file:
            file.write(tomlkit.dumps(conf))


def lda(args):
    terms_file = args.terms_file
    preproc_file = args.preproc_file
    output_dir = args.outdir
    output_dir.mkdir(exist_ok=True)

    placeholder = args.placeholder
    relevant_prefix = placeholder

    if args.no_relevant:
        labels = ('keyword',)
    else:
        labels = ('keyword', 'relevant')

    docs, titles = prepare_documents(preproc_file, terms_file,
                                     labels, args.target_column, args.title,
                                     delimiter=args.delimiter,
                                     placeholder=placeholder,
                                     relevant_prefix=relevant_prefix)

    if args.load_model is not None:
        lda_path = Path(args.load_model)
        try:
            model = LdaModel.load(str(lda_path / 'model'))
            dictionary = Dictionary.load(str(lda_path / 'model_dictionary'))
        except FileNotFoundError as err:
            msg = 'Error: file {!r} not found'
            sys.exit(msg.format(err.filename))

    else:
        no_below = args.no_below
        no_above = args.no_above
        topics = args.topics
        try:
            alpha = float(args.alpha)
        except ValueError:
            alpha = args.alpha
        else:
            if alpha < MIN_ALPHA_VAL:
                sys.exit('Error: alpha cannot be less than 1e-20')
        try:
            beta = float(args.beta)
        except ValueError:
            beta = args.beta

        seed = args.seed
        model, dictionary = train_lda_model(docs, topics, alpha, beta,
                                            no_above, no_below, seed)

    topics, docs_topics, avg_topic_coherence = prepare_topics(model, docs,
                                                              titles,
                                                              dictionary)

    print(f'Average topic coherence: {avg_topic_coherence:.4f}.')
    u = str(uuid.uuid4())
    output_topics(topics, docs_topics, output_dir, 'lda', u,
                  use_timestamp=not args.no_timestamp)

    if args.model:
        lda_path: Path = args.outdir / 'lda_model'
        lda_path.mkdir(exist_ok=True)
        model.save(str(lda_path / 'model'))
        dictionary.save(str(lda_path / 'model_dictionary'))


def main():
    parser = init_argparser()
    args = parser.parse_args()
    if args.config is not None:
        try:
            with open(args.config) as file:
                config = tomlkit.loads(file.read())
        except FileNotFoundError:
            msg = 'Error: config file {} not found'
            sys.exit(msg.format(args.config))

        from slrkit import prepare_script_arguments
        args, _, _ = prepare_script_arguments(config, args.config.parent,
                                              args.config.name,
                                              parser.slrkit_arguments)
        # handle the outdir parameter
        param = Path(config.get('outdir', Path.cwd()))
        setattr(args, 'outdir', param.resolve())
    lda(args)


if __name__ == '__main__':
    main()
