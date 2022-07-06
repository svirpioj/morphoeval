"""Methods for co-occurrence based evaluation"""

import logging

import munkres
import numpy as np
from scipy.sparse import csr_matrix
import tqdm

from .common import vector_recall


logger = logging.getLogger(__name__)


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


def strict_comma_eval(gold_sim, pred_sim, beta=1):
    """Make optimal match for alternative gold and pred analyses and return scores"""
    logger.debug(pred_sim.toarray().T)
    logger.debug(gold_sim.toarray().T)
    gold_altnum = gold_sim.shape[1]
    pred_altnum = pred_sim.shape[1]
    if gold_altnum == 1 and pred_altnum == 1:
        rec_val, rec_nz = vector_recall(gold_sim, pred_sim)
        pre_val, pre_nz = vector_recall(pred_sim, gold_sim)
    else:
        n_max = max(gold_altnum, pred_altnum)
        recalls = np.zeros((n_max, n_max))
        precisions = np.zeros((n_max, n_max))
        costs = np.ones((n_max, n_max))
        for gold_idx in range(gold_altnum):
            for pred_idx in range(pred_altnum):
                rec, rec_nz_t = vector_recall(gold_sim[:, gold_idx], pred_sim[:, pred_idx])
                pre, pre_nz_t = vector_recall(pred_sim[:, pred_idx], gold_sim[:, gold_idx])
                if rec_nz_t == 0:
                    rec = 0
                if pre_nz_t == 0:
                    pre = 0
                fscore = (1 + beta**2) * pre * rec / (beta**2 * pre + rec) if pre + rec > 0 else 0
                recalls[gold_idx, pred_idx] = rec
                precisions[gold_idx, pred_idx] = pre
                costs[gold_idx, pred_idx] = 1 - fscore
        indexes = munkres.Munkres().compute(costs)
        if n_max > 1:
            logger.debug("Costs:\n%s", costs)
            logger.debug("Matching: %s", indexes)
        pre_t, rec_t = 0, 0
        for gold_idx, pred_idx in indexes:
            pre_t += precisions[gold_idx, pred_idx].item()
            rec_t += recalls[gold_idx, pred_idx].item()
        pre_val = pre_t / pred_altnum
        rec_val = rec_t / gold_altnum
        rec_nz = (gold_sim.sum(0) > 0).sum()
        pre_nz = (pred_sim.sum(0) > 0).sum()
    logger.debug("rec: %s %s", rec_val, rec_nz)
    logger.debug("pre: %s %s", pre_val, pre_nz)
    return pre_val, rec_val, pre_nz, rec_nz


def comma_strict(goldlist, predlist, diagonals=False, beta=1):
    """Return precision and recall from CoMMA-S"""
    word_index = predlist.get_word_index()
    pre_sum, rec_sum, pre_n, rec_n = 0, 0, 0, 0
    for word in tqdm.tqdm(predlist.analyses):
        pred_sim = predlist.word_similarity_matrix(word, word_index, diagonals=diagonals)
        gold_sim = goldlist.word_similarity_matrix(word, word_index, diagonals=diagonals)
        logger.debug(word)
        pre_val, rec_val, pre_nz, rec_nz = strict_comma_eval(gold_sim, pred_sim, beta=beta)
        if rec_nz > 0:
            rec_sum += rec_val
            rec_n += 1
        if pre_nz > 0:
            pre_sum += pre_val
            pre_n += 1
        logger.debug("rec: %s %s", rec_sum, rec_n)
        logger.debug("pre: %s %s", pre_sum, pre_n)
    pre = pre_sum / pre_n if pre_n > 0 else 1.0
    rec = rec_sum / rec_n if rec_n > 0 else 1.0
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
