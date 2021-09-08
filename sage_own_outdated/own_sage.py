import random
import numpy as np
import pandas as pd
from helper import rf_marginal
import networkx as nx


class CGsage:
    """SAGE values for input model and data
    TODO: description
    """

    def __init__(self, x, y, model, loss, x_sample, dsep_test=False, adj_mat=None, outer=10, inner=10, seed=None):
        self.x = x
        self.y = y
        self.model = model
        self.loss = loss
        self.x_sample = x_sample
        self.dsep_test = dsep_test
        self.adj_mat = adj_mat
        self.outer = outer
        self.inner = inner
        self.seed = seed

    def sage_fn(self):
        if self.seed is not None:
            np.random.seed(self.seed)
            random.seed(self.seed)
        '''method to compute the values'''
        if self.dsep_test:
            g = nx.DiGraph(self.adj_mat)
        col_names = self.x.columns.to_list()
        sage = np.zeros(len(self.x.iloc[0]))
        # initiate feature indices to be permuted
        feature_inds = np.arange(0, len(self.x.iloc[0]))
        # initiate dataframe to track sage across runs
        track_sage = pd.DataFrame(columns=col_names)
        # outer_iter to keep track of outer loop
        outer_iter = 1
        while outer_iter < self.outer + 1:
            # draw a random index (i.e. observation) TODO random state
            index = random.randint(0, len(self.x) - 1)
            # get a permutation of the features (column indices but numbers) TODO random state
            rand_perm = np.random.permutation(feature_inds)
            # initiate coalition vectors
            S = np.zeros(len(self.x.iloc[0]))
            loss_prev = self.loss(y_true=[self.y.iloc[index]], y_pred=[rf_marginal(self.x, self.model)], labels=[0, 1, 2])
            # make a copy of X_ for current loop
            X_ = self.x_sample.copy()
            # from the current permutation, make a SAGE summand for every feature (with increasing
            # coalition size for every later feature)
            for i in range(len(rand_perm)):
                dsep = False
                if self.dsep_test:
                    if i == 0:
                        # col_names[rand_perm[i]] name of added feature
                        dsep = nx.d_separated(g, {col_names[rand_perm[i]]}, {str(self.y.name)}, set())
                    else:
                        cond_set = {col_names[rand_perm[0]]}
                        for z in range(i - 1):
                            cond_set.add(col_names[rand_perm[z + 1]])
                        dsep = nx.d_separated(g, {col_names[rand_perm[i]]}, {str(self.y.name)}, cond_set)
                if dsep:
                    # SAGE summand for current feature given previous features
                    delta = 0
                else:
                    # for current observation (index), use rand_perm[i] for the current feature's value
                    current_val = self.x.iloc[index, rand_perm[i]]
                    # S at the position of the respective feature is assigned the current value (for the observation)
                    # this is updated for every feature until looped through all and going back to outer loop
                    S[rand_perm[i]] = current_val
                    # from the sampling data drop these not adhering to the values of the current coalition (condition)
                    X_ = X_[X_[str(col_names[rand_perm[i]])] == current_val]
                    # initiate the current prediction
                    current_pred = 0
                    # copy of S for the inner loop
                    S_ = np.copy(S)
                    inner_iter = 0
                    while inner_iter < self.inner:
                        # loop to randomly sample (naive conditional sampling) the remaining features (not S or current)
                        for j in range(i + 1, len(self.x.iloc[0])):
                            # get index for the feature
                            ind = rand_perm[j]
                            ind_str = str(col_names[rand_perm[j]])
                            # conditional vector (that adheres current observations) to sample feature value from
                            cond_vector = X_[ind_str]
                            cond_vector = cond_vector.reset_index(drop=True)
                            S_[ind] = random.choice(cond_vector)
                        # make another copy of S_ TODO necessary?
                        S__ = [S_]
                        # model prediction with S
                        current_pred = current_pred + self.model.predict_proba(S__)
                        inner_iter += 1
                    # averaged prediction
                    current_pred = current_pred / self.inner
                    # current loss
                    current_loss = self.loss(y_true=[self.y.iloc[index]], y_pred=current_pred, labels=[0, 1, 2])
                    delta = loss_prev - current_loss
                    loss_prev = current_loss
                # increment sage value for current feature by its delta
                sage[rand_perm[i]] = sage[rand_perm[i]] + delta
            # to track sage values
            sage_ = np.copy(sage)
            sage_ = sage_ / outer_iter
            data_to_append = {}
            # loop through the number of columns
            for p in range(len(self.x.iloc[0])):
                data_to_append[track_sage.columns[p]] = sage_[p]
            track_sage = track_sage.append(data_to_append, ignore_index=True)
            outer_iter += 1
        sage = sage / self.outer
        return sage

