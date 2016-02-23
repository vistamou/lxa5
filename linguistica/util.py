# -*- encoding: utf8 -*-

import json

from itertools import groupby


ENCODING = 'utf8'

SUFFIXING_LANGUAGES = {'english', 'french', 'hungarian', 'turkish', 'russian',
                       'german', 'spanish', 'test'}

PREFIXING_LANGUAGES = {'swahili'}

SEP_SIG = '/'           # separator between affixes in a sig (NULL/s/ed/ing)
SEP_SIGTRANSFORM = '.'  # separator between sig and affix (NULL-s-ed-ing.ed)
SEP_NGRAM = '\t'        # separator between words in an ngram
# (e.g. 'the\tunited\tstates' means the 3-gram 'the united states')

NULL = 'NULL'

# ------------------------------------------------------------------------------
# parameters, with the "factory settings"

# What programs use what parameters:
#
# ngram:     max_word_tokens
# signature: min_stem_length, max_affix_length, min_sig_count
# phon:      (no parameters so far)
# trie:      min_stem_length, min_affix_length, min_sf_pf_count
# manifold:  max_word_types, n_neighbors, n_eigenvectors, min_context_count
# (See the individual programs for what these parameters mean.)

PARAMETERS = {'max_word_tokens': 0,  # zero means all word tokens
              'min_stem_length': 4,
              'max_affix_length': 4,
              'min_sig_count': 5,
              # 'min_affix_length': 1,
              # 'min_sf_pf_count': 3,
              'n_neighbors': 9,
              'n_eigenvectors': 11,
              'min_context_count': 3,
              'max_word_types': 1000,
              'suffixing': 1,  # 1 means yes, 0 means no
              }

PARAMETERS_FILENAME = 'parameters.json'

# keep the following dicts for command line mode?

PROGRAMS = {'all', 'signature', 'ngram', 'trie', 'phon', 'manifold'}

PROGRAM_TO_DESCRIPTION = {
    'ngram': 'This program extracts word n-grams.',
    'signature': 'This program computes morphological signatures.',
    'phon': 'This program extracts phon n-grams and works on phonotactics.',
    'trie': 'This program computes tries and successor/predecessor '
            'frequencies.',
    'manifold': 'This program computes word neighbors.',
}

PROGRAM_TO_PARAMETERS = {
    'ngram': ['max_word_tokens'],

    'signature': ['max_word_tokens', 'min_stem_length', 'max_affix_length',
                  'min_sig_count'],

    'phon': ['max_word_tokens'],

    'trie': ['max_word_tokens', 'min_stem_length', 'min_affix_length',
             'min_sf_pf_count'],

    'manifold': ['max_word_types', 'n_neighbors', 'n_eigenvectors',
                 'min_context_count'],

    'all': ['max_word_tokens', 'min_stem_length', 'max_affix_length',
            'min_sig_count', 'min_affix_length', 'min_sf_pf_count',
            'n_neighbors', 'n_eigenvectors', 'min_context_count',
            'max_word_types'],
}


def fix_punctuations(line):
    line = line.replace('.', ' . ')
    line = line.replace(',', ' , ')
    line = line.replace(';', ' ; ')
    line = line.replace('!', ' ! ')
    line = line.replace('?', ' ? ')
    line = line.replace(':', ' : ')
    line = line.replace(')', ' ) ')
    line = line.replace('(', ' ( ')
    return line


def double_sorted(input_object, key=lambda x: x, reverse=False,
                  subkey=lambda x: x, subreverse=False):
    if not input_object:
        print("Warning: object is empty. Sorting aborted.")
        return

    new_sorted_list = list()
    sorted_list = sorted(input_object, key=key, reverse=reverse)

    for k, group in groupby(sorted_list, key=key):  # groupby from itertools

        # must use "list(group)", cannot use just "group"!
        sublist = sorted(list(group), key=subkey, reverse=subreverse)
        # see python 3.4 documentation:
        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        # "The returned group is itself an iterator that shares the underlying
        # iterable with groupby(). Because the source is shared, when the 
        # groupby() object is advanced, the previous group is no longer visible.
        # So, if that data is needed later, it should be stored as a list"

        new_sorted_list.extend(sublist)

    return new_sorted_list


def output_latex_table(iter_obj, file, title=None, headers=None,
                       row_functions=None, index=True):
    """
    Output LaTeX table code for *iter_obj* to *file*.

    :param iter_obj: an iterable object
    :param file: a file object (e.g. open(...))
    :param title: table title str
    :param headers: list of headers
    :param row_functions: list of row cell rendering functions.
        Each function takes only one argument and returns a str.
    :param index: whether the table has an index column; defaults to True.
    """
    if not title:
        title = 'Untitled table'
    if not headers:
        headers = ['header']
    if not row_functions:
        row_functions = [lambda x: str(x)]

    if len(headers) != len(row_functions):
        raise ValueError('headers and row_format not of the same size')

    if index:
        headers = ['Index'] + headers

    number_of_columns = len(headers)

    print(title, file=file)
    print('\\begin{{tabular}}{{{}}}'.format('l' * number_of_columns), file=file)
    print('\\toprule', file=file)
    print('{} \\\\'.format(' & '.join(headers)))
    print('\\midrule', file=file)

    for i, row_obj in enumerate(iter_obj, 1):
        if index:
            row_list = [str(i)]
        else:
            row_list = list()

        for row_func in row_functions:
            row_list.append(row_func(row_obj))

        print(' & '.join(row_list), file=file)

    print('\\bottomrule', file=file)
    print('\\end{tabular}\n', file=file)


def is_complex(s):
    """
    Test if string *s* is a complex number.
    """
    try:
        test = complex(s)
    except (ValueError, TypeError):
        return False
    else:
        return True


class LinguisticaJSONEncoder(json.JSONEncoder):
    """
    We define this custom JSONEncoder subclass to deal with what the standard
    json encoder cannot deal with:

    - set: change it into an array
    - complex number: get the real part only
    See example here: https://docs.python.org/3/library/json.html
    """
    def default(self, obj):
        if type(obj) is set:
            return sorted(obj)
        elif type(obj) is tuple:
            return list(obj)
        elif type(obj) not in {int, float} and is_complex(obj):
            return obj.real
        return json.JSONEncoder.default(self, obj)


def json_dump(obj, outfile_opened, ensure_ascii=False, indent=2,
              separators=(',', ': '), sort_keys=True,
              cls=LinguisticaJSONEncoder):
    """
    json.dump with our preferred parameters
    """
    json.dump(obj, outfile_opened, ensure_ascii=ensure_ascii, indent=indent,
              sort_keys=sort_keys, separators=separators, cls=cls)
