"""Added d-separation test"""

# TODO Add seed to make cg sage and sage comparable

import numpy as np
import pandas as pd
from sage import utils, core
from tqdm.auto import tqdm
import networkx as nx   # (CL)


class PermutationEstimator:
    """
    Estimate SAGE values by unrolling permutations of feature indices.

    Args:
      imputer: model that accommodates held out features.
      loss: loss function ('mse', 'cross entropy').
    """
    def __init__(self,
                 imputer,
                 loss='cross entropy',
                 dsep_test=False,
                 adj_mat=None,
                 col_names=None,
                 target=None,
                 track_deltas=False):
        self.imputer = imputer
        self.loss_fn = utils.get_loss(loss, reduction='none')
        self.dsep_test = dsep_test
        self.adj_mat = adj_mat
        self.col_names = col_names
        self.target = target
        self.track_deltas = track_deltas

    def __call__(self,
                 X,
                 Y=None,
                 batch_size=1,  # TODO batch_size back to 512
                 detect_convergence=False,
                 thresh=0.025,
                 n_permutations=1000,
                 min_coalition=0.0,
                 max_coalition=1.0,
                 verbose=False,
                 bar=True):
        """
        Estimate SAGE values.

        Args:
          X: input data.
          Y: target data. If None, model output will be used.
          batch_size: number of examples to be processed in parallel, should be
            set to a large value.
          detect_convergence: whether to stop when approximately converged.
          thresh: threshold for determining convergence.
          n_permutations: number of permutations to unroll.
          min_coalition: minimum coalition size (int or float).
          max_coalition: maximum coalition size (int or float).
          verbose: print progress messages.
          bar: display progress bar.

        The default behavior is to detect convergence based on the width of the
        SAGE values' confidence intervals. Convergence is defined by the ratio
        of the maximum standard deviation to the gap between the largest and
        smallest values.

        Returns: Explanation object.
        """

        # Determine explanation type.
        if Y is not None:
            explanation_type = 'SAGE'
        else:
            explanation_type = 'Shapley Effects'

        # Verify model.
        N, _ = X.shape
        num_features = self.imputer.num_groups
        X, Y = utils.verify_model_data(self.imputer, X, Y, self.loss_fn,
                                       batch_size)

        # Determine min/max coalition sizes.
        if isinstance(min_coalition, float):
            min_coalition = int(min_coalition * num_features)
        if isinstance(max_coalition, float):
            max_coalition = int(max_coalition * num_features)
        assert min_coalition >= 0
        assert max_coalition <= num_features
        assert min_coalition < max_coalition
        if min_coalition > 0 or max_coalition < num_features:
            relaxed = True
            explanation_type = 'Relaxed ' + explanation_type
        else:
            relaxed = False
            sample_counts = None

        # Possibly force convergence detection.
        if n_permutations is None:
            n_permutations = 1e20
            if not detect_convergence:
                detect_convergence = True
                if verbose:
                    print('Turning convergence detection on')

        if detect_convergence:
            assert 0 < thresh < 1

        # Set up bar.
        n_loops = int(n_permutations / batch_size)
        if bar:
            if detect_convergence:
                bar = tqdm(total=1)
            else:
                bar = tqdm(total=n_loops * batch_size * num_features)

        # CL track deltas
        if self.track_deltas:
            if self.col_names is None:
                raise ValueError("Delta tracking requires column names")
            # initiate df to track deltas, corresponding coalition and if applicable d-sep status
            foi_tracker = []
            coalition_tracker = []
            single_deltas = []
            if self.dsep_test:
                d_sep_tracker = []

        # Setup.
        arange = np.arange(batch_size)
        scores = np.zeros((batch_size, num_features))
        S = np.zeros((batch_size, num_features), dtype=bool)
        permutations = np.tile(np.arange(num_features), (batch_size, 1))
        tracker = utils.ImportanceTracker()

        if self.dsep_test:
            g = nx.DiGraph(self.adj_mat)
            nodes = list(g.nodes)
            assert self.target in nodes
            nodes.remove(self.target)
            assert self.col_names == nodes
        # Permutation sampling.
        for it in range(n_loops):
            # Sample data. (CL: N is number of obs, i.e. you draw batch_size observations)
            mb = np.random.choice(N, batch_size)    # CL: mb is vector of indices for obs
            x = X[mb]
            y = Y[mb]

            # Sample permutations.
            S[:] = 0
            for i in range(batch_size):
                np.random.shuffle(permutations[i])  # CL: as many permutations of the features as batches
            # CL: permutations[i] is now a shuffled array of numeric feature indices

            # Calculate sample counts.
            if relaxed:
                scores[:] = 0
                sample_counts = np.zeros(num_features, dtype=int)
                for i in range(batch_size):
                    sample_counts[permutations[i, min_coalition:max_coalition]] = (
                        sample_counts[permutations[i, min_coalition:max_coalition]] + 1)

            # Add necessary features to minimum coalition.
            for i in range(min_coalition):
                # Add next feature.
                inds = permutations[:, i]
                S[arange, inds] = 1

            # Make prediction with minimum coalition. (CL: here baseline)
            y_hat = self.imputer(x, S)
            prev_loss = self.loss_fn(y_hat, y)

            # Add all remaining features.
            for i in range(min_coalition, max_coalition):
                current_coalition = {self.col_names[permutations[0][min_coalition]]}
                for j in range(min_coalition, i):
                    current_coalition.add(self.col_names[permutations[0][j]])
                if self.track_deltas:
                    foi_tracker.append(self.col_names[permutations[0][i]])
                    coalition_tracker.append(current_coalition)

                # Add next feature.
                inds = permutations[:, i]   # CL: batch_size observations for feature i
                S[arange, inds] = 1
                # TODO can you do this batch wise?
                # CL I need from permutations[i] the permutations[i][j] number as index for col_names
                # then I can also go through all batch_sizes
                if self.dsep_test:
                    if i == 0:
                        dsep = nx.d_separated(g, {self.col_names[permutations[0][i]]}, {self.target}, set())
                    else:
                        cond_set = {self.col_names[permutations[0][min_coalition]]}
                        for j in range(min_coalition, i):
                            cond_set.add(self.col_names[permutations[0][j]])
                        dsep = nx.d_separated(g, {self.col_names[permutations[0][i]]}, {self.target}, cond_set)
                    if self.track_deltas:
                        d_sep_tracker.append(dsep)
                    if dsep:
                        scores[arange, inds] = 0
                        if self.track_deltas:
                            single_deltas.append(0)
                    else:
                        # Make prediction with missing features.
                        y_hat = self.imputer(x, S)
                        loss = self.loss_fn(y_hat, y)
                        scores[arange, inds] = prev_loss - loss
                        if self.track_deltas:
                            single_deltas.append(prev_loss - loss)
                        prev_loss = loss

                else:
                    # Make prediction with missing features.
                    y_hat = self.imputer(x, S)
                    loss = self.loss_fn(y_hat, y)
                    scores[arange, inds] = prev_loss - loss
                    if self.track_deltas:
                        single_deltas.append(prev_loss - loss)
                    prev_loss = loss


                # Update bar (if not detecting convergence).
                if bar and (not detect_convergence):
                    bar.update(batch_size)

            # Update tracker.
            tracker.update(scores, sample_counts)

            # Calculate progress.
            std = np.max(tracker.std)
            gap = max(tracker.values.max() - tracker.values.min(), 1e-12)
            ratio = std / gap

            # Print progress message.
            if verbose:
                if detect_convergence:
                    print(f'StdDev Ratio = {ratio:.4f} '
                          f'(Converge at {thresh:.4f})')
                else:
                    print(f'StdDev Ratio = {ratio:.4f}')

            # Check for convergence.
            if detect_convergence:
                if ratio < thresh:
                    if verbose:
                        print('Detected convergence')

                    # Skip bar ahead.
                    if bar:
                        bar.n = bar.total
                        bar.refresh()
                    break

            # Update convergence estimation.
            if bar and detect_convergence:
                N_est = (it + 1) * (ratio / thresh) ** 2
                bar.n = np.around((it + 1) / N_est, 4)
                bar.refresh()

        if bar:
            bar.close()

        if self.track_deltas:
            delta_tracker = pd.DataFrame()
            delta_tracker["foi"] = foi_tracker
            delta_tracker["coalition"] = coalition_tracker
            delta_tracker["deltas"] = single_deltas
            if self.dsep_test:
                delta_tracker["d-separated"] = d_sep_tracker

            return core.Explanation(tracker.values, tracker.std, explanation_type), delta_tracker
        else:
            return core.Explanation(tracker.values, tracker.std, explanation_type)
