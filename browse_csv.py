import pandas as pd
import argparse
import pickle

parser = argparse.ArgumentParser(
    description="browse csv")

parser.add_argument(
    "-p",
    "--path",
    type=str,
    default="file.csv",
    help="normal csv?",
)

parser.add_argument(
    "-pi",
    "--pickle",
    type=bool,
    default=False,
    help="pickled?",
)


args = parser.parse_args()

if args.pickle:
    df = pickle.load(open(args.path, "rb"))
else:
    df = pd.read_csv(args.path)
