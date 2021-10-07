import pickle
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx

path = "results_py/true_amat/dag_l.p"


class Lol:
    def __init__(self, path):
        self.path = path

    def load_g(self):
        g = pickle.load(open(self.path, "rb"))
        return g


if __name__ == "__main__":
    a = Lol(path)
