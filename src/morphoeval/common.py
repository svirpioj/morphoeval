"""Common classes and methods for the evaluation metrics"""

import collections
import logging

import numpy as np
from scipy.sparse import lil_matrix
import tqdm


logger = logging.getLogger(__name__)


def vector_recall(gold, pred):
    """Calculate recall from boundary vectors"""
    if gold.shape != pred.shape:
        raise ValueError(f"Vectors do not have the same shape: {gold.shape} {pred.shape}")
    total = gold.sum()
    if not total:
        return 1.0, total
    diff = gold - pred
    error = (abs(diff) + diff) / 2
    return ((gold - error).sum() / total).item(), total


class MorphSeq(list):
    """Sequence of morphs"""

    def unique(self):
        """Return unique morphs"""
        return sorted(self.counts())

    def counts(self):
        """Return morph counts"""
        return collections.Counter(self)

    def boundaries(self):
        """Return boundary vector (0 = no boundary, 1 = boundary)"""
        vsize = len(''.join(self)) - 1
        vect = np.zeros(vsize, dtype=int)
        idx = -1
        for morph in self:
            idx += len(morph)
            if idx < vsize:
                vect[idx] = 1
        return vect


class AnalysisSet:
    """Morphological analyses for a set of words"""

    def __init__(self):
        self.analyses = collections.defaultdict(list)
        self.morphs = {}
        self.n_morphs = 0

    def __contains__(self, word):
        return word in self.analyses

    @classmethod
    def from_file(cls, inputfile, vocab=None):
        """Create AnalysisSet from file"""
        obj = cls()
        obj.load(inputfile, vocab=vocab)
        return obj

    def add(self, word, analysis):
        """Add analysis for a word"""
        mseq = MorphSeq(analysis)
        for morph in mseq.unique():
            if morph not in self.morphs:
                self.morphs[morph] = self.n_morphs
                self.n_morphs += 1
        self.analyses[word].append(mseq)

    def load(self, inputfile, vocab=None):
        """Load segmentations from given input file object

        Given a container vocab, load only the words found in it.

        """
        for line in tqdm.tqdm(inputfile):
            if line[0] == '#':
                continue
            word, rest = line.split("\t")
            if vocab and word not in vocab:
                continue
            for alternative in rest.split(', '):
                self.add(word, alternative.split())

    def get_word_index(self):
        """Return index for the current set of words"""
        return {word: idx for idx, word in enumerate(self.analyses)}

    def to_word_morpheme_matrix(self, word_index, selected_alternatives=None, binary=True):
        """Return bipartite word-morpheme graph as a sparse matrix"""
        n_words = len(word_index)
        array = lil_matrix((n_words, self.n_morphs), dtype=int)
        for word, analyses in tqdm.tqdm(self.analyses.items()):
            if word not in word_index:
                continue
            vec = np.zeros(self.n_morphs)
            if selected_alternatives:
                analyses = [analyses[selected_alternatives[word]]]
            for mseq in analyses:
                if binary:
                    for morph in mseq.unique():
                        vec[self.morphs[morph]] = 1
                else:
                    for morph, count in mseq.counts().items():
                        vec[self.morphs[morph]] += count
            array[word_index[word], :] = vec
        return array.tocsr()

    def to_word_matrix(self, word_index, diagonals=False):
        """Return word graph as a sparse matrix

        Quick but can use a lot of memory.

        """
        logger.info("Creating word-morpheme matrix")
        word_morpheme_graph = self.to_word_morpheme_matrix(word_index)
        logger.info("Creating word-word matrix")
        word_graph = word_morpheme_graph @ word_morpheme_graph.T
        if not diagonals:
            word_graph.setdiag(0)
        return word_graph

    @staticmethod
    def common_morphs_array(analysis1, analysis2):
        """Return the number of common morphs for each alternative in two analyses"""
        array = np.zeros((len(analysis1), len(analysis2)), dtype=int)
        for idx1, mseq in enumerate(analysis1):
            counts1 = mseq.counts()
            for idx2, mseq2 in enumerate(analysis2):
                counts2 = mseq2.counts()
                array[idx1, idx2] = sum(min(counts2[morph], count) for morph, count in counts1.items())
        return array

    def word_similarity_matrix(self, word, word_index, diagonals=False):
        """Return the similarity of all analyses of word to other words"""
        n_words = len(word_index)
        analyses = self.analyses[word]
        array = lil_matrix((n_words, len(analyses)), dtype=int)
        for word2, analyses2 in tqdm.tqdm(self.analyses.items()):
            if word not in word_index:
                continue
            if word == word2 and not diagonals:
                continue
            array[word_index[word2], :] = self.common_morphs_array(analyses, analyses2).max(1)
        return array.tocsr()

    @staticmethod
    def common_morphs(analysis1, analysis2):
        """Return the maximum number of common morphs in two analyses"""
        max_ = 0
        for mseq in analysis1:
            counts1 = mseq.counts()
            for mseq2 in analysis2:
                counts2 = mseq2.counts()
                sum_ = sum(min(counts2[morph], count) for morph, count in counts1.items())
                max_ = max(sum_, max_)
        return max_

    def to_word_matrix_direct(self, word_index, diagonals=False):
        """Return word graph as a sparse matrix

        Memory-efficient but slow.

        """
        n_words = len(word_index)
        array = lil_matrix((n_words, n_words), dtype=int)
        for word, analysis in tqdm.tqdm(self.analyses.items()):
            if word not in word_index:
                continue
            vec = np.zeros(n_words)
            # logger.debug("%s %s", word, morphset)
            for word2, analysis2 in self.analyses.items():
                if word2 not in word_index:
                    continue
                if not diagonals and word2 == word:
                    continue
                common = self.common_morphs(analysis, analysis2)
                if common > 0:
                    vec[word_index[word2]] = common
            array[word_index[word], :] = vec
        return array.tocsr()
