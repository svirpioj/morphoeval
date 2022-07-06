#!/usr/bin/env python3
"""Command-line interface for morphoeval"""

import argparse
import logging

import ruamel.yaml

from .common import AnalysisSet
from . import comma, comma_strict, emma2, bpr, bpr_strict


logger = logging.getLogger(__name__)


def main():
    """Main method"""
    parser = argparse.ArgumentParser(description='Evaluation for morphological analysis and segmentation')
    parser.add_argument('--metric', '-m',
                        choices=['comma-b0', 'comma-b1', 'comma-s0', 'comma-s1', 'emma-2', 'bpr', 'bpr-s'],
                        default='comma-b0', help='metric (default %(default)s)')
    parser.add_argument('--beta', metavar='FLOAT', type=float, default=1, help='beta for using F_beta score')
    parser.add_argument('--verbose', '-v', action='store_true', help='increase verbosity')
    parser.add_argument('goldfile', type=argparse.FileType('r'), help='gold standard analysis file')
    parser.add_argument('predfile', type=argparse.FileType('r'), help='predicted analysis file')
    parser.add_argument('output', type=argparse.FileType('w'), nargs='?', default='-', help='output file')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    logger.info("Loading gold standard analyses")
    goldlist = AnalysisSet.from_file(args.goldfile)
    logger.info("Loading predicted analyses")
    predlist = AnalysisSet.from_file(args.predfile, vocab=goldlist)
    if args.metric == 'emma-2':
        pre, rec = emma2(goldlist, predlist)
    elif args.metric == 'comma-b1':
        pre, rec = comma(goldlist, predlist, diagonals=True)
    elif args.metric == 'comma-b0':
        pre, rec = comma(goldlist, predlist, diagonals=False)
    elif args.metric == 'comma-s1':
        pre, rec = comma_strict(goldlist, predlist, diagonals=True, beta=args.beta)
    elif args.metric == 'comma-s0':
        pre, rec = comma_strict(goldlist, predlist, diagonals=False, beta=args.beta)
    elif args.metric == 'bpr-s':
        pre, rec = bpr_strict(goldlist, predlist, beta=args.beta)
    else:
        pre, rec = bpr(goldlist, predlist)
    output = {
        'metric': args.metric,
        'files': {'reference': args.goldfile.name, 'predictions': args.predfile.name},
        'scores': {'precision': round(pre, 4), 'recall': round(rec, 4)}
    }
    fscore = (1 + args.beta**2) * pre * rec / (args.beta**2 * pre + rec) if pre + rec > 0 else 0
    if args.beta == 1:
        output['scores']['f-score'] = round(fscore, 4)
    else:
        output['scores']['f_beta-score'] = round(fscore, 4)
        output['scores']['beta'] = args.beta
    ruamel_yaml = ruamel.yaml.YAML(typ='safe', pure=True)
    ruamel_yaml.dump(output, stream=args.output)


if __name__ == '__main__':
    main()
