# -*- coding: utf-8 -*-


__version__ = '0.3.2'
from indago._optimizer import Optimizer, CandidateState
from indago._utility import minimize, minimize_exhaustive, inspect, inspect_optimizers

from indago._pso import PSO
from indago._fwa import FWA
from indago._ssa import SSA
from indago._de import DE
from indago._ba import BA
from indago._efo import EFO
from indago._mrfo import MRFO
from indago._direct_search import MSGS

optimizers = [PSO, FWA, SSA, DE, BA, EFO, MRFO, MSGS]
optimizers_name_list = [o.__name__ for o in optimizers]
optimizers_dict = {o.__name__: o for o in optimizers}

# Undocumented optimizers
from indago._mmo import MMO
from indago._abca import ABC
from indago._direct_search import NelderMead




