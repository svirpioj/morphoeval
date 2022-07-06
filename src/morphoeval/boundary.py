"""Methods for boundary evaluation"""

import logging

import munkres
import numpy as np
import tqdm

from .common import vector_recall


logger = logging.getLogger(__name__)


def boundary_recall(gold, predicted):
    """Calculate boundary recall

    Uses the best local match for alternative segmentations.

    """
    total = 0
    hits = 0
    for word, gold_alternatives in tqdm.tqdm(gold.analyses.items()):
        if len(word) < 2:
            # Skip single letter words
            continue
        best = 0
        for gold_mseq in gold_alternatives:
            gold_v = gold_mseq.boundaries()
            if gold_v.sum() == 0:
                best = 1
                break
            for pred_mseq in predicted.analyses[word]:
                rec, _ = vector_recall(gold_v, pred_mseq.boundaries())
                if rec > best:
                    best = rec
        total += 1
        hits += best
    return hits / total


def bpr(goldlist, predlist):
    """Return boundary precision and recall (bpr)"""
    logger.info("Calculating precision")
    pre = boundary_recall(predlist, goldlist)
    logger.info("Calculating recall")
    rec = boundary_recall(goldlist, predlist)
    return pre, rec


def best_strict_boundary_recall(gold_alternatives, pred_alternatives, beta=1):
    """Find optimal matching between the alternatives and return scores"""
    n_gold = len(gold_alternatives)
    n_pred = len(pred_alternatives)
    n_max = max(n_gold, n_pred)
    recalls = np.zeros((n_max, n_max))
    precisions = np.zeros((n_max, n_max))
    costs = np.ones((n_max, n_max))
    for gold_idx, gold_mseq in enumerate(gold_alternatives):
        for pred_idx, pred_mseq in enumerate(pred_alternatives):
            rec, _ = vector_recall(gold_mseq.boundaries(), pred_mseq.boundaries())
            pre, _ = vector_recall(pred_mseq.boundaries(), gold_mseq.boundaries())
            fscore = (1 + beta**2) * pre * rec / (beta**2 * pre + rec) if pre + rec > 0 else 0
            recalls[gold_idx, pred_idx] = rec
            precisions[gold_idx, pred_idx] = pre
            costs[gold_idx, pred_idx] = 1 - fscore
    indexes = munkres.Munkres().compute(costs)
    if n_max > 1:
        word = ''.join(gold_alternatives[0])
        logger.debug("Costs for word %s:\n%s", word, costs)
        logger.debug("Matching for word %s: %s", word, indexes)
    pre_t, rec_t = 0, 0
    for gold_idx, pred_idx in indexes:
        pre_t += precisions[gold_idx, pred_idx].item()
        rec_t += recalls[gold_idx, pred_idx].item()
    return pre_t / n_pred, rec_t / n_gold


def bpr_strict(goldlist, predlist, beta=1):
    """Return boundary precision and recall (bpr) with strict matching"""
    pre_total, rec_total = 0, 0
    pre_hits, rec_hits = 0, 0
    for word, gold_alternatives in tqdm.tqdm(goldlist.analyses.items()):
        if len(word) < 2:
            # Skip single letter words
            continue
        pre_score, rec_score = best_strict_boundary_recall(
            gold_alternatives, predlist.analyses[word], beta=beta)
        pre_hits += pre_score
        rec_hits += rec_score
        pre_total += 1
        rec_total += 1
    return pre_hits / pre_total, rec_hits / rec_total
