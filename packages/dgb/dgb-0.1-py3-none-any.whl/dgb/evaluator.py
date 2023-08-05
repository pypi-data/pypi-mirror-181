"""
An evaluator for dynamic link prediction task

Date:
    - Oct. 30, 2022
    - Dec. 06, 2022
"""

import torch
import numpy as np
from sklearn.metrics import *

np.seterr(divide='ignore', invalid='ignore')


class Evaluator(object):
    """An Evaluator for Dynamic Link Prediction Task"""

    def __init__(self):
        super(Evaluator, self).__init__()

    def _parse_and_check_input(self, input_dict):
        """
        check whether the input has the required format
        @param: input_dict: a dictionary containing "y_true", "y_pred", and "eval_metric"
                note: "eval_metric" should be a list including one or more of the followin metrics:
                    [ap, au_roc_score, au_pr_score, acc, prec, rec, f1]
        """
        valid_metric_list = ['ap', 'au_roc_score', 'au_pr_score', 'acc', 'prec', 'rec', 'f1']

        if 'eval_metric' not in input_dict:
            raise RuntimeError("Missing key of eval_metric")

        for eval_metric in input_dict['eval_metric']:
            if eval_metric in valid_metric_list:
                if 'y_true' not in input_dict:
                    raise RuntimeError('Missing key of y_true')
                if 'y_pred' not in input_dict:
                    raise RuntimeError('Missing key of y_pred')

                y_true, y_pred = input_dict['y_true'], input_dict['y_pred']

                # converting to numpy on cpu
                if torch is not None and isinstance(y_true, torch.Tensor):
                    y_true = y_true.detach().cpu().numpy()
                if torch is not None and isinstance(y_pred, torch.Tensor):
                    y_pred = y_pred.detach().cpu().numpy()

                # check type and shape
                if not isinstance(y_true, np.ndarray) or not isinstance(y_pred, np.ndarray):
                    raise RuntimeError("Arguments to Evaluator need to be either numpy ndarray or torch tensor!")

                if not y_true.shape == y_pred.shape:
                    raise RuntimeError("Shape of y_true and y_pred must be the same!")

            else:
                print("ERROR: The evaluation metric should be in:", valid_metric_list)
                raise ValueError('Undefined eval metric %s ' % (eval_metric))

        return y_true, y_pred

    def get_measures_for_threshold(self, y_true, y_pred, threshold):
        """
        compute measures for a specific threshold
        """
        perf_measures = {}
        y_pred_label = y_pred > threshold
        perf_measures['acc'] = accuracy_score(y_true, y_pred_label)
        prec, rec, f1, num = precision_recall_fscore_support(y_true, y_pred_label, average='binary', zero_division=1)
        perf_measures['prec'] = prec
        perf_measures['rec'] = rec
        perf_measures['f1'] = f1
        return perf_measures

    def _compute_metrics(self, y_true, y_pred):
        """
        compute the performance metrics for the given true labels and prediction probabilities
        @param: y_true: actual true labels
        @param: y_pred: predicted probabilities
        """
        perf_dict = {'ap': average_precision_score(y_true, y_pred), 'au_roc_score': roc_auc_score(y_true, y_pred)}

        prec_pr_curve, rec_pr_curve, pr_thresholds = precision_recall_curve(y_true, y_pred)
        perf_dict['au_pr_score'] = auc(rec_pr_curve, prec_pr_curve)

        # predifined threshold = 0.5
        perf_half_dict = self.get_measures_for_threshold(y_true, y_pred, 0.5)
        perf_dict['acc'] = perf_half_dict['acc']
        perf_dict['prec'] = perf_half_dict['prec']
        perf_dict['rec'] = perf_half_dict['rec']
        perf_dict['f1'] = perf_half_dict['f1']

        return perf_dict

    def eval(self, input_dict, verbose=False):
        """
        evaluation for dynamic link prediction task
        """
        y_true, y_pred = self._parse_and_check_input(input_dict)
        perf_dict = self._compute_metrics(y_true, y_pred)

        if verbose:
            print("INFO: Evaluation Results:")
            for eval_metric in input_dict['eval_metric']:
                print(f"\t>>> {eval_metric}: {perf_dict[eval_metric]:.4f}")

        return perf_dict


def main():
    """
    A code snipet to check the evaluator functionality
    Please consider this code only as an example, and feel free to modify it according to your requirements
    """
    evaluator = Evaluator()

    # y_true & y_pred: ndarray of shape (n_samples,)
    # y_true: shows the status of existence of an edge: 0: negative edge, 1: positive edge
    # y_pred: the probability of existence of an edge; output of a dynamic graph learning model

    # here, we randomly generate two arrays to check the evaluator functionality
    np.random.seed(42)
    y_true = np.random.randint(2, size=100)
    y_pred = np.random.random_sample((100,))

    # the evaluation metrics should be in the following list (note: it should be passed as a list)
    evaluation_metric_list = ['ap', 'au_roc_score', 'au_pr_score', 'acc', 'prec', 'rec', 'f1']
    input_dict = {'y_true': y_true,
                  'y_pred': y_pred,
                  'eval_metric': evaluation_metric_list
                  }
    eval_result = evaluator.eval(input_dict, verbose=True)
    print(eval_result)

if __name__ == '__main__':
    main()
