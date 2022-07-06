# morphoeval - Evaluation for morphological analysis and segmentation

## Introduction

This package provides re-implementations for the BPR, CoMMA, and
EMMA-2 evaluation methods for unsupervised morphological analysis and
segmentation introduced by Virpioja et al. (2011).

The BPR (boundary precision and recall) method calculates a
macro-average of the segmentation boundary matches over the words and
is thus suitable for evaluating unsupervised or supervised
morphological segmentation.

The CoMMA and EMMA-2 methods are designed for the task of unsupervised
morphological analysis that was the goal in the Morpho Challenge
competitions organized between 2005 and 2010 (see Kurimo et al.,
2010). The challenge in the evaluation of unsupervised morphological
analysis is that the predicted morphemes labels and the labels in gold
standard analysis are not directly comparable, as an unsupervised
algorithm does not see the gold standard labels, and in contrast to
unsupervised morphological segmentation, the labels are not simply
subsequences of words.

Both methods start with a bipartite morpheme-word graph that collects
the occurrences of the morphemes in the word forms within the test
set. The CoMMA methods first use the morpheme-word graphs to create
word graphs, with edges as co-occurring morphemes, for the predicted
and gold standard analyses, and calculates the precision and recall of
the edges. The EMMA (Spiegler and Monson, 2010) and EMMA-2 methods use
the morpheme-word graph to make one-to-one or one-to-many assignments
between the predicted and gold standard morphemes, and calculates the
precision and recall based on the mapped morphemes.

## The choice of method

The choice of the evaluation method should depend on the task at hand
(segmentation or analysis) and whether the method produces (and the
gold standard includes) multiple alternative analyses per word. Here
are our recommendations; see Virpioja et al. (2011) for further
discussion.

| Task                       | Single analysis per word | Multiple analyses per word |
|----------------------------|--------------------------|----------------------------|
| Morphological segmentation | BPR                      | BPR-S                      |
| Morphological analysis     | EMMA-2, CoMMA-B0         | EMMA-2, CoMMA-S0           |

## Usage

Installing the package provides a single command, `morphoeval`:

```
$ morphoeval --help
usage: morphoeval [-h] [--metric {comma-b0,comma-b1,comma-s0,comma-s1,emma-2,bpr,bpr-s}] [--verbose]
                     goldfile predfile [output]

Metrics for morphological analysis and segmentation

positional arguments:
  goldfile              gold standard analysis file
  predfile              predicted analysis file
  output                output file

optional arguments:
  -h, --help            show this help message and exit
  --metric {comma-b0,comma-b1,comma-s0,comma-s1,emma-2,bpr,bpr-s}, -m {comma-b0,comma-b1,comma-s0,comma-s1,emma-2,bpr,bpr-s}
                        metric (default comma-b0)
  --beta FLOAT          beta for using F_beta score
  --verbose, -v         increase verbosity
```

The parameters are simple enough: Use `--metric` to select the
evaluation method that you want to use, and provide the gold standard
and predicted analysis files.

The input files should be in the format used in Morpho Challenges:
The word and its analyses are separated by a tabular character, any
alternative analyses by a comma and a space, and the labels of the
analyses by single space. For example:

```
brush	brush_N
brushes	brush_N +3SG, brush_N +PL
```

The output is written in YAML format:

```yaml
files: {predictions: pred.txt, reference: gold.txt}
metric: emma-2
scores: {f-score: 0.9251, precision: 0.8939, recall: 0.9585}
```

Note: For large (>10k words) input files, running the evaluation may
take a considerable amount of memory.

## Original scripts

The original scripts are available at
http://morpho.aalto.fi/events/morphochallenge/, but do not work with
modern Python versions. The current implementation has the following
limitations compared to the previous scripts:

- The original EMMA algorithm with one-to-one mapping between
  morphemes is not supported.
- Weighting of each input word is not supported.

## References

References as BibTeX:

```
% Kurimo et al. (2010)
@inproceedings{kurimo-et-al-2010-morpho,
    address = {Uppsala, Sweden},
    author = {Mikko Kurimo and Sami Virpioja and Ville Turunen and Krista Lagus},
    booktitle = {Proceedings of the 11th Meeting of the ACL Special Interest Group on Computational Morphology and Phonology},
    month = {July},
    pages = {87--95},
    publisher = {Association for Computational Linguistics},
    title = {Morpho Challenge 2005-2010: Evaluations and Results},
    url = {https://aclanthology.org/W10-2211},
    year = {2010},
}

% Spiegler and Monson (2010)
@inproceedings{spiegler-monson-2010-emma,
    address = {Beijing, China},
    author = {Sebastian Spiegler and Christian Monson},
    booktitle = {Proceedings of the 23rd International Conference on Computational Linguistics (Coling 2010)},
    month = {August},
    pages = {1029--1037},
    publisher = {Coling 2010 Organizing Committee},
    title = {{EMMA}: A novel Evaluation Metric for Morphological Analysis},
    url = {https://aclanthology.org/C10-1116},
    year = {2010},
}

% Virpioja et al. (2011)
@article{virpioja-et-al-2011-empirical,
    author = {Sami Virpioja and Ville T. Turunen and Sebastian Spiegler and Oskar Kohonen and Mikko Kurimo},
    journal = {Traitement Automatique des Langues},
    number = {2},
    pages = {45--90},
    publisher = {ATALA},
    title = {Empirical Comparison of Evaluation Methods for Unsupervised Learning of Morphology},
    url = {https://www.atala.org/sites/default/files/TAL_52_2_2.pdf},
    volume = {52},
    year = {2011},
}
```
