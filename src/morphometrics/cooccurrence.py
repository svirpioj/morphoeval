"""Methods for co-occurrence based evaluation"""

import collections
import logging

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
import tqdm


logger = logging.getLogger(__name__)


class MorphSeq(list):
    """Sequence of morphs"""

    def unique(self):
        """Return unique morphs"""
        return sorted(self.counts())

    def counts(self):
        """Return morph counts"""
        return collections.Counter(self)


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


def word_graph_recall(gold, pred):
    """Calucate recall from word co-occurrence graph"""
    totals = gold.sum(1)
    diff = gold - pred
    error = (abs(diff) + diff) / 2
    recall = (gold - error).sum(1)
    with np.errstate(divide='ignore', invalid='ignore'):
        recall = recall / totals
    recall = recall[~np.isnan(recall)]
    return recall.mean().item() if recall.shape[1] else 1.0


def comma(goldlist, predlist, diagonals=False):
    """Return precision and recall from CoMMA"""
    windex = predlist.get_word_index()
    gold_word_graph = goldlist.to_word_matrix(windex, diagonals=diagonals)
    pred_word_graph = predlist.to_word_matrix(windex, diagonals=diagonals)
    logger.debug("Gold word graph:\n%s", gold_word_graph.toarray())
    logger.debug("Pred word graph:\n%s", pred_word_graph.toarray())
    logger.info("Calculating precision")
    pre = word_graph_recall(pred_word_graph, gold_word_graph)
    logger.info("Calculating recall")
    rec = word_graph_recall(gold_word_graph, pred_word_graph)
    return pre, rec


def morph_assignment_matrix(morph_cooc_graph):
    """Return sparse morph assignment matrix"""
    assign = morph_cooc_graph.argmax(axis=1).A1  # A1 is equivalent to np.asarray(x).ravel()
    logger.debug("Assignment vector: %s", assign)
    dim = assign.shape[0]
    return csr_matrix((np.ones(dim), (assign, np.arange(dim))),
                      shape=(morph_cooc_graph.shape[1], dim), dtype=int)


def morph_graph_recall(gold, pred):
    """Calucate recall from morph co-occurrence graph"""
    gold_totals = gold.sum(1)
    pred_totals = pred.sum(1)
    diff = gold_totals - pred_totals
    error = (abs(diff) + diff) / 2
    recall = (gold_totals - error).sum(1)
    with np.errstate(divide='ignore', invalid='ignore'):
        recall = recall / gold_totals
    recall = recall[~np.isnan(recall)]
    return recall.mean().item() if recall.shape[1] else 1.0


def emma2(goldlist, predlist):
    """Return precision and recall from EMMA-2"""
    windex = predlist.get_word_index()
    logger.info("Creating gold word-morpheme matrix")
    gold_word_morpheme_graph = goldlist.to_word_morpheme_matrix(windex, binary=False)
    logger.info("Creating pred word-morpheme matrix")
    pred_word_morpheme_graph = predlist.to_word_morpheme_matrix(windex, binary=False)
    logger.info("Creating morph co-occurrence matrix")
    morph_cooc_graph = gold_word_morpheme_graph.T @ pred_word_morpheme_graph  # size (M_gold, M_pred)
    logger.debug(morph_cooc_graph.shape)
    logger.debug("Gold morphs: %s", goldlist.morphs)
    logger.debug("Pred morphs: %s", predlist.morphs)
    logger.debug("Morph co-occurrence graph:\n%s", morph_cooc_graph.toarray())
    logger.info("Calculating precision")
    # When calculating precision, several predicted morphemes may assigned to one reference morpheme
    assign = morph_assignment_matrix(morph_cooc_graph.T)
    logger.debug("Pred word-morpheme matrix:\n%s", pred_word_morpheme_graph.toarray())
    logger.debug("Assignments:\n%s", assign.toarray())
    gold_to_pred = gold_word_morpheme_graph @ assign  # Gold mapped to pred morphs
    logger.debug("Gold mapped to pred:\n%s", gold_to_pred.toarray())
    pre = morph_graph_recall(pred_word_morpheme_graph, gold_to_pred)
    logger.debug(pre)
    logger.info("Calculating recall")
    # When calculating recall, several reference morphemes may assigned to one predicted morpheme
    assign = morph_assignment_matrix(morph_cooc_graph)
    logger.debug("Gold word-morpheme matrix:\n%s", gold_word_morpheme_graph.toarray())
    logger.debug("Assignments:\n%s", assign.toarray())
    pred_to_gold = pred_word_morpheme_graph @ assign  # Gold mapped to pred morphs
    logger.debug("Pred mapped to gold:\n%s", pred_to_gold.toarray())
    rec = morph_graph_recall(gold_word_morpheme_graph, pred_to_gold)
    logger.debug(rec)
    return pre, rec
