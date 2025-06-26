from __future__ import print_function
from easygui import *
import networkx as nx
import numpy as np
import pandas as pd
import sys
import os
import datetime
import inspect
import sys
import subprocess
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


# debug handle
#
# debug -> False: off
# debug -> True: on

debug = False


tree_graph = nx.DiGraph()
temp_tree_graph = nx.DiGraph()
temp_tree = nx.DiGraph()
reduced_tree_graph = nx.DiGraph()


def getLineInfo():
    print("    ^-- ", inspect.stack()[1][1], ":", inspect.stack()[1][2], ":",
          inspect.stack()[1][3])


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

