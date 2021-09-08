from functions import d_separation


class GraphComparison:
    """Simple class to compare two nx.DiGraphs w.r.t. to their d-separation (w.r.t. target y)"""
    def __init__(self, g_true, g_est, y, mc=None, rand_state=None):
        self.g_true = g_true
        self.g_est = g_est
        self.y = y
        self.mc = mc
        self.rand_state = rand_state

    def exact(self):
        true_dseps = d_separation(self.g_true, self.y)
        est_dseps = d_separation(self.g_est, self.y)
        # now compare every entry
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for i in range(true_dseps.shape[0]):
            for j in range(true_dseps.shape[1]):
                if true_dseps.iloc[i, j] == est_dseps.iloc[i, j]:
                    if true_dseps.iloc[i, j] is True:
                        tp += 1
                    else:
                        tn += 1
                else:
                    if true_dseps.iloc[i, j] is True:
                        fn += 1
                    else:
                        fp += 1

        # total number of d-separations in true graph
        d_separated_total = tp + fn
        d_connected_total = tn + fp
        return tp, tn, fp, fn, d_separated_total, d_connected_total

    def approx(self):
        true_dseps = d_separation(self.g_true, self.y, mc=self.mc, random_state=self.rand_state)
        est_dseps = d_separation(self.g_est, self.y, mc=self.mc, random_state=self.rand_state)
        # now compare every entry
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for i in range(len(true_dseps)):
            if true_dseps == est_dseps:
                if true_dseps is True:
                    tp += 1
                else:
                    tn += 1
            else:
                if true_dseps is True:
                    fn += 1
                else:
                    fp += 1

        # total number of d-separation among tested nodes (make a node if d-separations were approximated via mc)
        d_separated_total = tp + fn
        d_connected_total = tn + fp
        return tp, tn, fp, fn, d_separated_total, d_connected_total
