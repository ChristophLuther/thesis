from itertools import combinations
import pandas as pd
import networkx as nx
import random
import math
import numpy as np
import os
from scipy.stats import bernoulli


def powerset(items):
    """computes power set of iterable object items

    Args:
        items: iterables object, e.g. list, array

    Returns:
         power set of items
    """

    combo = []
    for r in range(len(items) + 1):
        # use a list to coerce an actual list from the combinations generator
        combo.append(list(combinations(items, r)))
    return combo


# function for all d separations wrt target:
def d_separation(g, y, mc=None, random_state=None):
    """Test d-separation of single node and y given every possible conditioning set in graph g

    Args:
        g : nx.DiGraph
        y : target node with respect to which d-separation is tested
        mc : if int given, mc sampling a subset of d-separations to be tested, recommended for large graphs
        random_state : seed for random and np.random when mc is not None

    Returns:
         pandas dataframe of boolean values for d-separation for every node except y (if mc is None)
         boolean array of d-separation, not comprehensible w.r.t. which d-separations were tested explicitly
         (if mc is not None)
    """
    # list of nodes (strings)
    predictors = list(g.nodes)
    # sort list to get consistent results across different graphs learned on same features (when using mc)
    predictors.sort()
    # remove the target from list of predictors
    predictors.remove(y)
    n = len(predictors)

    # TODO remove everything that is 'too large'
    # number of possible d-separations between one feature and target, i.e. number of potential conditioning sets
    if mc is None:
        no_d_seps = (2 ** (n-1))
    # initiate dataframe for all d-separations
    d_separations = pd.DataFrame(index=predictors, columns=range(no_d_seps))
    # initiate list for d_separations

    if mc is not None:
        if random_state is not None:
            random.seed(random_state)
            np.random.seed(random_state)
            rng = np.random.default_rng(seed=random_state)
        else:
            rng = np.random.default_rng()
        # initiate vector to store True/False for d-separations (cannot track conditioning sets)
        d_seps_bool = []
        # get a vector of probabilities to draw the size of the conditioning set; note that for n-1 potential
        # deconfounders there are n different sizes of conditioning sets because of the empty set
        probs = []
        for i in range(n):
            probs.append((math.comb(n-1, i)) / (2**(n-1)))
        k = 0
        while k < mc:
            # draw index for feature of interest
            ind = random.randint(0, n-1)
            # retrieve feature of interest
            node = predictors[ind]
            # list of all features but feature of interest
            deconfounders = list(g.nodes)
            deconfounders.remove(y)
            deconfounders.remove(node)
            # sample a conditioning set from deconfounders
            # draw a cardinality
            card = np.random.choice(np.arange(n), p=probs)
            if card == 0:
                # test d-separation with empty set as conditioning set
                cond_set = set()
                d_seps_bool.append(nx.d_separated(g, {node}, {y}, cond_set))
            else:
                # draw as many as 'card' numbers from range(n-1) as indices for conditioning set
                indices = rng.choice(n-1, size=card, replace=False)
                cond_set = set()
                for ii in range(len(indices)):
                    # index for first
                    index = indices[ii]
                    cond_set.add(deconfounders[index])
                d_seps_bool.append(nx.d_separated(g, {node}, {y}, cond_set))
            k += 1
        return d_seps_bool
    else:
        for i in range(n):
            # test d-separation w.r.t. target using all conditional sets possible
            # for current predictor at i-th position in predictors
            node = predictors[i]
            deconfounders = list(g.nodes)
            deconfounders.remove(y)
            deconfounders.remove(node)
            power_set = powerset(deconfounders)
            j = 0
            while j < no_d_seps:
                for k in range(len(power_set)):
                    # k == 0 refers to the empty set in power_set
                    if k == 0:
                        cond_set = set()
                        d_separations.iloc[i, j] = nx.d_separated(g, {node}, {y}, cond_set)
                        j += 1
                    else:
                        for jj in range(len(power_set[k])):
                            cond_set = {power_set[k][jj][0]}
                            for m in range(len(power_set[k][jj]) - 1):
                                cond_set.add(power_set[k][jj][m + 1])
                            d_separations.iloc[i, j] = nx.d_separated(
                                g, {node}, {y}, cond_set
                            )
                            j += 1
        return d_separations


# compute the number of d-separation statements from n

def dsep_mb(n, mb):
    """computes a lower bound for the number of d-separation statements between a target node
    and every other node in the graph given the size of the target node's Markov blanket

    Args:
        n: number of nodes in graph
        mb: size of Markov blanket of target

    Returns:
        Lower bound for number of d-separations
    """

    # number of nodes other than y and Markov blanket: n-1-mb
    # number of d-separations for such nodes 2**(n-2-mb)
    return (n - 1 - mb) * 2 ** (n - 2 - mb)


def dsep_degree(n, max_degree, sink=False):
    """computes a lower bound for the number of d-separation statements between a target node
        and every other node in the graph given the max degree of a node

        Args:
            n : number of nodes in graph
            max_degree : maximal degree of a node in the graph (max. number of edges associated to a node
            sink : Bool, whether target is sink node or not
        Returns:
            Lower bound for number of d-separations
        """
    if sink is False:
        # maximal size of Markov blanket
        max_mb = max_degree + max_degree ** 2
        return dsep_mb(n, max_mb)
    else:
        max_mb = max_degree
        return dsep_mb(n, max_mb)


def potential_dseps(n):
    """For a graph of size n, return the maximal number of d-separations between each node and a potentially
    dedicated target node

    Args:
        n: number of nodes in graph

    Return:
        Number of potential d-separation statements (float)
    """
    return (n - 1) * (2 ** (n - 2))


def create_folder(directory):
    """Creates directory as specified in function argument if not already existing

    Args:
        directory: string specifying the directory
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory: " + directory)


def create_amat(n, p):
    """Create a custom adjacency matrix of size n x n

    Args:
        n: number of nodes
        p: probability of existence of an edge for each pair of nodes

    Returns:
        Adjacency matrix as pd.DataFrame

    """
    # create col_names
    variables = []
    for i in range(n):
        variables.append(str(i+1))

    # create df for amat
    amat = pd.DataFrame(columns=variables, index=variables)

    # TODO avoid double loop (use zip)
    for j in range(n):
        for k in range(n):
            amat.iloc[j, k] = bernoulli(p)
