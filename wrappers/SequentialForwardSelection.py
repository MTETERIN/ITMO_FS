#!/usr/bin/env python

import random as rnd

import numpy as np
from sklearn.linear_model import LinearRegression
from filters import RandomFilter



class SequentialForwardSelection:
    """
        Sequentially Adds Features that Maximises the Classifying function when combined with the features already used

        Parameters
        ----------
        estimator: object
            A supervised learning estimator with a fit method that provides information about feature importance either
            through a coef_ attribute or through a feature_importances_ attribute.
        n_features : int
            Number of features to select.

        See Also
        --------


        Examples
        --------

        """

    def __init__(self, estimator, n_features, seed=1):
        self.estimator_ = estimator
        self.n_features_ = n_features
        self.features_ = []
        rnd.seed(seed)

    def fit(self, X, y, test_x, test_y):
        """
            Fits wrapper.

            Parameters
            ----------
            X : array-like, shape (n_features,n_samples)
                The training input samples.
            y : array-like, shape (n_features,n_samples)
                the target values.
            percentage : float, number of training cases that has to be checked for prediction
            Returns
            ------
            None

            See Also
            --------
            Examples
            --------

        """
        accuracy = 0
        current_features = np.array([])

        for feature in X[0:1,:]:
            old_features = current_features
            current_features = np.append(current_features, feature)
            self.estimator_.fit([X[i] for i in current_features], y)

            current_accuracy = self.get_current_accuracy(X, current_features, test_x, test_y)

            if accuracy > current_accuracy:
                self.features_ = current_features
            else:
                current_features = old_features

    def get_current_accuracy(self, X, current_features, test_x, test_y):
        correct = 0
        for i in range(test_x.length):
            predict = self.estimator_.predict([X[j] for j in current_features])
            if predict == test_y[i]:
                correct += 1
        current_accuracy = correct / test_x.length
        return current_accuracy

    def predict(self, X):
        self.estimator_.predict([X[i] for i in self.features_])


fil = SequentialForwardSelection(LinearRegression(), 8)
print(fil.fit(np.ones((5, 10)), np.ones(10)))
print(fil.predict(np.ones((5, 5))))
