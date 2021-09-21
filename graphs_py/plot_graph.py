import pickle
import networkx as nx
import matplotlib.pyplot as plt


path = "results_py/hc/est_amat/dag_m_10000_obs.p"


class Lol:
    def __init__(self, path):
        self.path = path

    def load_amat(self):
        amat = pickle.load(open(self.path, "rb"))
        return amat


if __name__ == "__main__":
    a = Lol(path)
