import logging
import os

import bioc
import tqdm


def scan_document(*_, **kwargs):
    """
    Scan each document in a list of BioC source files, apply fn, and print to directory.

    Args:
        kwargs:
            source(list): a list of source pathnames
            directory(str): output directory
            fn:
                fn should expect the following arguments in this given order:
                    sequence1
                    sequence2
                    ...
                    non_sequence1
                    non_sequence2
                    ...
            verbose(boolean):
    """
    source = kwargs.pop('source')
    verbose = kwargs.pop('verbose', True)
    directory = os.path.expanduser(kwargs.pop('directory'))
    suffix = kwargs.pop('suffix')
    fn = kwargs.pop('fn')
    non_sequences = kwargs.pop('non_sequences', None)

    for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose):
        basename = os.path.splitext(os.path.basename(pathname))[0]
        dstname = os.path.join(directory, '{}{}'.format(basename, suffix))
        with open(pathname) as fp:
            collection = bioc.load(fp)
            for document in collection.documents:
                try:
                    args = [document] + non_sequences
                    fn(*args)
                except:
                    logging.exception('Cannot process %s', document.id)
        with open(dstname, 'w') as fp:
            bioc.dump(collection, fp)


def scan_collection(*_, **kwargs):
    """
        Scan each document in a list of BioC source files, apply fn, and print to directory.

        Args:
            kwargs:
                source(list): a list of source pathnames
                directory(str): output directory
                fn:
                    fn should expect the following arguments in this given order:
                        sequence1
                        sequence2
                        ...
                        non_sequence1
                        non_sequence2
                        ...
                verbose(boolean):
        """
    source = kwargs.pop('source')
    verbose = kwargs.pop('verbose', True)
    directory = os.path.expanduser(kwargs.pop('directory'))
    suffix = kwargs.pop('suffix')
    fn = kwargs.pop('fn')
    non_sequences = kwargs.pop('non_sequences', None)

    for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose):
        basename = os.path.splitext(os.path.basename(pathname))[0]
        dstname = os.path.join(directory, '{}{}'.format(basename, suffix))
        with open(pathname) as fp:
            collection = bioc.load(fp)
            try:
                args = [collection] + non_sequences
                fn(*args)
            except:
                logging.exception('Cannot process %s', collection.source)
        with open(dstname, 'w') as fp:
            bioc.dump(collection, fp)
