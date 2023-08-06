import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score


def compute_scores_thresholding(gt, exp, threshold):
    ret = np.max(exp) * threshold
    binary_exp_array = exp > ret

    TP = (binary_exp_array * gt).sum()
    predict_pos = binary_exp_array.sum()
    actual_pos = gt.sum()

    precision = TP / predict_pos
    recall = TP / actual_pos
    f1_score = (2 * precision * recall) / (precision + recall + 1e-6)

    return precision, recall, f1_score


def comptue_score_general(gt, exp):
    auc_score = roc_auc_score(gt.flatten(), exp.flatten())
    ap_score = average_precision_score(gt.flatten(), exp.flatten())
    return auc_score, ap_score


class PointGame():
    """Pointing Game Evaluation Method.

    This evaluator assumes that the explanation result should align with the visual objects. Based on this idea, the 
    evaluation is to compute the alignment between the bounding box or semantic segmentation with the explanations.

    PointGame computes the alignment to the bounding box. PointGameSegmentation computes the alignment to the 
    semantic segmentation.

    More details can be found in the original paper:
    https://arxiv.org/abs/1608.00507.

    Note that the bounding box of annotations is required for the evaluation. This method does not need models. For API
    compatibility, we implement it within the same functions as other evaluators.
    """

    def __init__(self):
        pass

    def evaluate(self, bbox: tuple, exp_array: np.ndarray, threshold=0.25) -> dict:
        """
        Since the explanation is actually a ranking order, PointGame computes two categories of measures. One is based
        on thresholding. Here, ``threshold`` * max(``exp_array``) is used as the threshold. Based on this, precision,
        recall and F1 score are computed, *w.r.t.* ``bbox``. Another measure does not depend on the threshold. Here, 
        the ROC AUC score and the Average Precision (both of them are imported from :py:mod:`sklearn.metrics`) are 
        computed.

        Args:
            bbox (tuple): A tuple of four integers: (x1, y1, x2, y2), where (x1, y1) is the coordinates of the top-left
                point *w.r.t.* width and height respectively; (x2, y2) is the coordinates of the bottom-right point 
                *w.r.t.* width and height respectively;
            exp_array (np.ndarray): the explanation result from an interpretation algorithm.
            threshold (float, optional): threshold for computing precision, recall and F1 score. Defaults to ``0.25``.

        Returns:
            dict: A dict containing ``precision``, ``recall``, ``f1_score`` and ``auc_score``, ``ap_score``, where the 
            first three depend on the threshold and the last two do not.
        """

        gt = np.zeros_like(exp_array, dtype=np.uint8)
        x1, y1, x2, y2 = bbox
        gt[y1:y2, x1:x2] = 1

        # depends on the threshold
        precision, recall, f1_score = compute_scores_thresholding(gt, exp_array, threshold)
        r = {'precision': precision, 'recall': recall, 'f1_score': f1_score}

        # independ of threshold
        auc_score, ap_score = comptue_score_general(gt, exp_array)
        r.update({'auc_score': auc_score, 'ap_score': ap_score})

        return r


class PointGameSegmentation():
    """Pointing Game Evaluation Method using Segmentation.

    This evaluator assumes that the explanation result should align with the visual objects. Based on this idea, the 
    evaluation is to compute the alignment between the bounding box or semantic segmentation with the explanations.

    PointGame computes the alignment to the bounding box. PointGameSegmentation computes the alignment to the 
    semantic segmentation.

    More details can be found in the original paper:
    https://arxiv.org/abs/1608.00507.

    Note that the semantic segmentation is required for the evaluation. This method does not need models. For API
    compatibility, we implement it within the same functions as other evaluators.
    """

    def __init__(self):
        pass

    def evaluate(self, seg_gt: np.ndarray, exp_array: np.ndarray, threshold=0.25) -> dict:
        """        
        Since the explanation is actually a ranking order, PointGameSegmentation computes two categories of measures.
        One is based on thresholding. Here, ``threshold`` * max(``exp_array``) is used as the threshold. Based on this,
        precision, recall and F1 score are computed, *w.r.t.* ``seg_gt``. Another measure does not depend on the 
        threshold. Here, the ROC AUC score and the Average Precision (both of them are imported from 
        :py:mod:`sklearn.metrics`) are computed.

        Args:
            seg_gt (np.ndarray): binary values are supported only currently.
            exp_array (np.ndarray): the explanation result from an interpretation algorithm.
            threshold (float, optional): threshold for computing precision, recall and F1 score. Defaults to ``0.25``.

        Returns:
            dict: A dict containing ``precision``, ``recall``, ``f1_score`` and ``auc_score``, ``ap_score``, where the 
            first three depend on the threshold and the last two do not.
        """
        gt = seg_gt

        # depends on the threshold
        precision, recall, f1_score = compute_scores_thresholding(gt, exp_array, threshold)
        r = {'precision': precision, 'recall': recall, 'f1_score': f1_score}

        # independ of threshold
        auc_score, ap_score = comptue_score_general(gt, exp_array)
        r.update({'auc_score': auc_score, 'ap_score': ap_score})

        return r
