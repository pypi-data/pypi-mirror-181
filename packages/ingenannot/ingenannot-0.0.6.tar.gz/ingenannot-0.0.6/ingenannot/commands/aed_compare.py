#/usr/bin/env python3

import logging
import multiprocessing
import math
import pysam
import sys
from ingenannot.utils import Utils
from ingenannot.utils.gff_reader import GFF3Reader, GTFReader
from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.annot_edit_distance import AnnotEditDistance
from ingenannot.utils.graphics import Graphics
from ingenannot.commands.command import Command

import numpy as np
#import seaborn as sns
import matplotlib
import pandas as pd
import re

import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg



class AEDCompare(Command):

    def __init__(self, args):

        self.fof = args.fof
        self.ncol = 6

    def run(self):
        """"launch command"""

        sources = Utils.get_sources_from_fof(self.fof)
        genes = Utils.extract_genes_from_fof(self.fof)
        Utils.get_aed_from_attributes(genes)
        Graphics.plot_cumulative_aed(sources, genes, "tr","cumulative_tr_AED.png",self.ncol)
        Graphics.plot_cumulative_aed(sources, genes, "pr","cumulative_pr_AED.png",self.ncol)
        Graphics.plot_cumulative_aed(sources, genes, "best","cumulative_best_AED.png",self.ncol)

        return 0
