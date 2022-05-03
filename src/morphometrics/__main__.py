#!/usr/bin/env python3
"""Command-line interface for morphometrics"""

import argparse
import logging

import ruamel.yaml

from . import AnalysisSet, comma, emma2


logger = logging.getLogger(__name__)


def main():
    """Main method"""
    parser = argparse.ArgumentParser(description='Metrics for unsupervised morphological analysis')
    parser.add_argument('--metric', '-m', choices=['comma-b0', 'comma-b1', 'emma-2'],
                        default='comma-b0', help='metric')
    parser.add_argument('--verbose', '-v', action='store_true', help='increase verbosity')
    parser.add_argument('goldFile', type=argparse.FileType('r'), help='gold standard analysis file')
    parser.add_argument('predFile', type=argparse.FileType('r'), help='predicted analysis file')
    parser.add_argument('output', type=argparse.FileType('w'), nargs='?', default='-', help='output file')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    logger.info("Loading gold standard analyses")
    goldlist = AnalysisSet.from_file(args.goldFile)
    logger.info("Loading predicted analyses")
    predlist = AnalysisSet.from_file(args.predFile, vocab=goldlist)
    if args.metric == 'emma-2':
        pre, rec = emma2(goldlist, predlist)
    elif args.metric == 'comma-b1':
        pre, rec = comma(goldlist, predlist, diagonals=True)
    else:
        pre, rec = comma(goldlist, predlist, diagonals=False)
    fscore = 2 * pre * rec / (pre + rec)
    ruamel_yaml = ruamel.yaml.YAML(typ='safe', pure=True)
    ruamel_yaml.dump({
        'metric': args.metric,
        'files': {'reference': args.goldFile.name, 'predictions': args.predFile.name},
        'scores': {'precision': round(pre, 4), 'recall': round(rec, 4), 'f-score': round(fscore, 4)}
    }, stream=args.output)


if __name__ == '__main__':
    main()
