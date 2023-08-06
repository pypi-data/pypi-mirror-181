"""
module metrics.py
----------------------
 Utility functions for calculating models' performce metrics.
"""
from sklearn import metrics
import numpy as np


def get_confusion_matrix(y_true, y_pred):
    """Calculates and returns the confusion matrix.

    :param y_true: the ground thruth targets.
    :param y_pred: the predictions made by the model.
    """
    return metrics.confusion_matrix(y_true, y_pred)


def get_mean_misclassification_error(y_true, y_pred):
    # accuracy = TP + TN / N
    accuracy = metrics.accuracy_score(y_true, y_pred)
    # MME = FP + FN / N   <->  ou 1 - accuracy
    return 1. - accuracy


def get_precision_recall_f1(y_true, y_pred):
    precision, recall, f1, _ = metrics.precision_recall_fscore_support(
        y_true, 
        y_pred, 
        average='binary',
        pos_label=1
    )
    return precision, recall, f1


def get_TPR_TNR_FNR_FPR(y_true, y_pred):
    # get confusion matrix
    cm  = get_confusion_matrix(y_true, y_pred).astype(np.float32)
    # True positives
    TP = cm[1,1]
    # False Negatives
    FN = cm[1, 0]
    # True Negatives
    TN = cm[0, 0]
    # Fasel Positive
    FP = cm[0, 1]
        
    
    #TPR (recall) = TP/(TP+FN)
    TPR = TP / (TP + FN)

    #TNR (True Negativa Rate) - specificity
    TNR = TN / (TN + FP)

    # False Negative Rate = 1 - TPR
    FNR = FN / (TP + FN)

    # False Positive Rate = 1 - TNR
    FPR = FP / (TN + FP)

    return TPR, TNR, FNR, FPR 

def get_PPV_NPV_FDR_FOR(y_true, y_pred, pos_label=1):
    # get confusion matrix
    cm  = get_confusion_matrix(y_true, y_pred)
    # True positives
    TP = cm[pos_label,pos_label]
    # True Negatives
    TN = cm[0, 0]
    # False Negatives
    FN = cm[pos_label, 0]
    # Fasel Positive
    FP = cm[0, pos_label]
    
    #PPV - Positive Predicted Value (precision) = TP/(TP+FP)
    PPV = TP / (TP + FP)

    #NPV (Negative Predicted Value)
    NPV = TN / (TN + FN)

    # False Discovery Rate = 1 - PPV(precision)
    FDR = FP / (TP + FP)

    # False Omission Rate = 1 - NPV
    FOR = FN / (TN + FN)

    return PPV, NPV, FDR, FOR 

def get_roc_curve(y_true, y_scores, pos_label=1):

    # return TPRs, FPRs, thresholds
    return metrics.roc_curve(
        y_true, 
        y_scores,
        pos_label=pos_label
    )

def get_roc_auc(y_true, y_scores):
    return metrics.roc_auc_score(y_true, y_scores)

def get_precision_recall_curve(y_true, y_scores, pos_label=1):
    # returns precisions, recalls, thresholds
    return metrics.precision_recall_curve(
        y_true,
        y_scores,
        pos_label=pos_label
    )

def get_average_precision_score(y_true, y_scores, pos_label=1):
    return metrics.average_precision_score(
        y_true, 
        y_scores,
        pos_label=pos_label
    )