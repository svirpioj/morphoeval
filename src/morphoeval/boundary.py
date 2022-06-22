"""Methods for boundary evaluation"""

import logging

import tqdm


logger = logging.getLogger(__name__)


def vector_recall(gold, pred):
    """Calculate recall from boundary vectors"""
    if gold.shape != pred.shape:
        raise ValueError(f"Vectors do not have the same shape: {gold.shape} {pred.shape}")
    total = gold.sum()
    if not total:
        return 1.0
    diff = gold - pred
    error = (abs(diff) + diff) / 2
    return ((gold - error).sum() / total).item()


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
                rec = vector_recall(gold_v, pred_mseq.boundaries())
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
