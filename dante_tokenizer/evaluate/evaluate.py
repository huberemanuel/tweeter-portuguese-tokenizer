import numpy as np


def longest_common_token_sequence(left: list, right: list) -> int:
    """
    Implementation of Longest Common Subsequence using lists of tokens
    instead of strings, hence Longest Common Token Sequence.

    Parameters
    ----------
    left: list
        First first of tokens
    right: list
        Second list of tokens
    i_left: int
        Index for iterating over left list
    i_right: int
        Index for iterating over right list

    Returns
    -------
    int
        Size of the Logest Common Token Sequence found.
    """

    n_left = len(left)
    n_right = len(right)

    L = [[None] * (n_right + 1) for i in range(n_left + 1)]

    for i in range(n_left + 1):
        for j in range(n_right + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif left[i - 1] == right[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[n_left][n_right]


def evaluate_dataset(
    pred_tokens: list, true_tokens: list, complete_metrics: bool = False
) -> (float, float):
    """
    Evaluate tokenizer's results, returning precision, recall, f-score and extra_metrics if
    `complete_metrics` is set to True.

    Parameters
    ----------
    pred_tokens: list
        List of predicted tokens.
    true_tokens: list
        List of true tokens.
    complete_metrics: bool
        If true, return aditional metrics.

    Returns
    -------
    ((float, float), (float, float), (float, float))
        Precision, Recall and F-score measurements (mean, std).
    """
    assert len(pred_tokens) == len(true_tokens)
    n_sents = len(pred_tokens)
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    incorrect_sentences_ids = []
    precision_scores = []
    recall_scores = []
    f_scores = []

    for i in range(n_sents):
        tp, fp, fn = evaluate_sentence(pred_tokens[i], true_tokens[i])
        true_positives += tp
        false_positives += fp
        false_negatives += fn
        precision_scores.append(tp / (tp + fp + 1e-9))
        recall_scores.append(tp / (tp + fn + 1e-9))
        f_scores.append(
            2
            * precision_scores[-1]
            * recall_scores[-1]
            / (precision_scores[-1] + recall_scores[-1] + 1e-9)
        )

        if fp > 0 or fn > 0:
            incorrect_sentences_ids.append(i)

    precision = (np.mean(precision_scores), np.std(precision_scores))
    recall = (np.mean(recall_scores), np.std(recall_scores))
    f_score = (np.mean(f_scores), np.std(f_scores))

    if complete_metrics:
        additional_metrics = {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "incorrect_sentences_ids": incorrect_sentences_ids,
        }
        return precision, recall, f_score, additional_metrics

    return precision, recall, f_score


def evaluate_sentence(pred_tokens: list, true_tokens: list) -> (int, int):
    """
    Calculates precision and coverage of tokens.
    Based on the Longest Common Subsequence Algorithm
    to evaluate pred_tokens and true_tokens, with the difference of
    not considering spaced substrings as matches.

    Examples
    --------
    >>> evaluate_sentence(["Oi", ":)"], ["Oi", ":)"])
    (2, 0, 0)

    Parameters
    ----------
    pred_tokens: list
        List of tokens generated by the tokenizer
    true_tokens: list
        List of true tokens

    Returns
    -------
    (int, int, int)
        True positive, false positives, false negatives
    """

    true_positives = longest_common_token_sequence(pred_tokens, true_tokens)
    false_positives = len(pred_tokens) - true_positives
    false_negatives = len(true_tokens) - true_positives

    return true_positives, false_positives, false_negatives
