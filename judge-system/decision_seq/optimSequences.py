
#import threading
#import subprocess
import pathlib
import shutil
import datetime
from timeit import default_timer as timer
import sys

#import hdsobol
import itertools
import random
import warnings

from qdpy import algorithms, containers, plots, base
#import os, time, multiprocessing, yaml, copy
#import psutil
#from sklearn.linear_model import LinearRegression

#from base import *
#import submitPepperCorn
#import submitNupack
#from algos import *
#import nupack_overlap
from qdpy.phenotype import Individual
from qdpy.base import registry, DomainLike
from typing import Any, Sequence

from qdpy.containers import *


def hamming_distance(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

class SequencesIndividual(Individual):
    def __init__(self, domains = None, **kwargs):
        super().__init__(**kwargs)
        self.domains = domains
        self.name = str(id(self))
        if self.domains is not None:
            self.random_init()

    def random_init(self):
        size = sum([len(d.sequence) for d in self.domains])
        self[:] = [random.choice("ATCG") for _ in range(size)]
        self.assemble()
        #print(f"DEBUG random_init: {self[:]} {size} {self.domains}")

    def domains_to_seq(self):
        return [d.sequence for d in self.domains]

    def assemble(self):
        if self.domains is None:
            return
        index = 0
        for d in self.domains:
            n = len(d.sequence)
            seq = self[index:index+n]
            index += n
            assert(len(seq) == n)
            d.sequence = "".join(seq)

    def is_valid(self, hamming_threshold = 2):
        if self.domains is None or len(self.domains) < 2:
            return False

        # Check if domains are sufficiently different (hamming distance < hamming_threshold)
        hamming_cond = False
        for i in range(len(self.domains)-1):
            for j in range(i+1, len(self.domains)):
                hamming_cond = hamming_distance(self.domains[i].sequence, self.domains[j].sequence) < hamming_threshold
                if hamming_cond:
                    break
            if hamming_cond:
                break

        # Check if domains are not rotations of each other
        rotation_cond = False
        for i in range(len(self.domains)-1):
            for j in range(i+1, len(self.domains)):
                for r in nupack_overlap.circ_perm(list(self.domains[i].sequence)):
                    rotation_cond = (''.join(r) == self.domains[j].sequence)
                    if rotation_cond:
                        break
                if rotation_cond:
                    break
            if rotation_cond:
                break

        return not hamming_cond and not rotation_cond



#@registry.register
#class GenSequencesIndividuals(GenIndividuals):
#    def __next__(self):
#        return SequencesIndividual()

def gen_sequences_individuals(domains):
    while(True):
        yield SequencesIndividual(domains)


def sel_roulette(collection: Sequence[Any]) -> Sequence[Any]:
    """Select and return one individual at random (using a roulette selection)

    Parameters
    ----------
    :param collection: Container
        The Container containing individuals.
    """
    assert(len(collection))
    sum_fit_val = [sum(i.fitness.values) for i in collection]
    sum_all_fit = sum(sum_fit_val)
    if sum_all_fit == 0:
        probs = [1. / len(collection) for _ in sum_fit_val]
    else:
        probs = [f / sum_all_fit for f in sum_fit_val]
    return random.choices(collection, weights=probs)[0]




@registry.register
class SequencesGA(algorithms.Evolution):
    def __init__(self, container: Container, budget: int,
            dimension: int, init_budget: int = 100,
            sel_pb: float = 1.0, init_pb: float = 0.0, 
            mut_nb_domain: DomainLike = [1, 3],
            domains = None, hamming_threshold = 2, **kwargs):
        self.init_budget = init_budget
        self.sel_pb = sel_pb
        self.init_pb = init_pb
        self.mut_nb_domain = mut_nb_domain
        self.domains = domains
        self.hamming_threshold = hamming_threshold
        #print(f"#### DEBUG domains: {self.domains} {[d.sequence for d in self.domains]}")

        # TODO add init_budget ?
        select_or_initialise = partial(tools.sel_or_init,
                #sel_fn = tools.sel_random,
                sel_fn = sel_roulette,
                sel_pb = sel_pb,
                init_fn = self._init,
                init_pb = init_pb)

        super().__init__(container, budget, dimension=dimension, # type: ignore
                select_or_initialise=select_or_initialise, vary=self._vary,
                base_ind_gen=gen_sequences_individuals(self.domains),
                **kwargs)

    def _init(self, base_ind):
        for j in range(10000):
            base_ind.random_init()
            if base_ind.is_valid(self.hamming_threshold):
                break
            #else:
            #    print(f"DEBUG init not valid: {base_ind}")
        if j >= 9999:
            raise RuntimeError("INIT: could not find valid inds")
        return base_ind

    def _vary(self, ind):
        for j in range(10000):
            ind2 = copy.deepcopy(ind)
            nb_muts = random.randint(*self.mut_nb_domain)
            indexes = list(range(len(ind2)))
            random.shuffle(indexes)
            indexes = indexes[:nb_muts]
            for i in indexes:
                possible_muts = list({'A', 'T', 'C', 'G'} - {ind2[i]})
                ind2[i] = random.choice(possible_muts)
            ind2.assemble()
            if ind2.is_valid(self.hamming_threshold):
                break
        if j >= 9999:
            raise RuntimeError("VARY: could not find valid inds")
        return ind2








# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
