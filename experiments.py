import os
import sys
import yaml
from config import exp_directory


class Experiment(object):
    pass


def main():
    exp_file = sys.argv(1)
    specs = yaml.load(open(os.path.join(exp_directory, exp_file), 'r').read())

    exp_type = specs["type"]



""" Tasks """
def embed_and_compare():
    pass


if __name__ == "__main__"():
    main()