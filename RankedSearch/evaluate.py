""" Assignment 2
"""
import abc

import numpy as np


class EvaluatorFunction:
    """
    An Abstract Base Class for evaluating search results.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, hits, relevant):
        """
        Do not modify.
        Params:
          hits...A list of document ids returned by the search engine, sorted
                 in descending order of relevance.
          relevant...A list of document ids that are known to be
                     relevant. Order is insignificant.
        Returns:
          A float indicating the quality of the search results, higher is better.
        """
        return


class Precision(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute precision. tp / (tp + fp)
        tp = relevant and retrieved
        tfp (tp+fp) = total retrieved
        >>> Precision().evaluate([1, 2, 3, 4], [2, 4])
        0.5
        """
        tfp = len(hits)
        tp = len(set(hits).intersection(relevant))

        if tfp == 0:
            return 0
        else:
            precision = tp/tfp
            return precision

    def __repr__(self):
        return 'Precision'


class Recall(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute recall. tp / (tp + fn)
        tp = relevant and retrieved
        tpfn (tp+fn) = total relevant
        >>> Recall().evaluate([1, 2, 3, 4], [2, 5])
        0.5
        >>> Recall().evaluate([n for n in range(1,6)], [n for n in range(10,16)])
        0.0
        """
        tp = len(set(hits).intersection(relevant))
        tpfn = len(relevant)
        
        if tpfn == 0:
            return 0
        else:
            recall = tp / tpfn
            return recall

    def __repr__(self):
        return 'Recall'


class F1(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute F1. 2PR/(P+R)

        >>> F1().evaluate([1, 2, 3, 4], [2, 5])  # doctest:+ELLIPSIS
        0.333...
        """
        precision = Precision().evaluate(hits, relevant)
        recall = Recall().evaluate(hits, relevant)
        pr = precision + recall
        if pr == 0:
            return 0
        else:
            f1 = (2*precision*recall)/pr
            return f1

    def __repr__(self):
        return 'F1'


class MAP(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute Mean Average Precision.

        >>> MAP().evaluate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 4, 6, 11, 12, 13, 14, 15, 16, 17])
        0.2
        """
        count = 0.0
        prec = 0.0
        den = len(relevant)
        if den == 0:
            return 0
        else:
            for index, h in enumerate(hits):
                if h in relevant:
                    count += 1
                    prec += count / (index+1)
            
            ave_precision = prec / den
            
            return ave_precision

    def __repr__(self):
        return 'MAP'

