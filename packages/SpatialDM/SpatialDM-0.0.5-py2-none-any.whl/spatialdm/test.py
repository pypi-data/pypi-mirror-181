import os
import pandas as pd
import numpy as np
import anndata as ann

from main import *
from diff_utils import *
import plottings as pl
# adata = dataset.melanoma()
# weight_matrix(adata, l=1.2, cutoff=0.2, single_cell=False) # weight_matrix by rbf kernel
# extract_lr(adata, 'human', min_cell=3)
# spatialdm_global(adata,1000, select_num=None, method='both', nproc=1)     # global Moran selection
# sig_pairs(adata, method='permutation', fdr=True, threshold=0.1)
# spatialdm_local(adata, n_perm=1000, method='both', select_num=None, nproc=1)     # local spot selection
# sig_spots(adata, method='permutation', fdr=False, threshold=0.1)     # significant local spots

from datasets import dataset

adata = dataset.melanoma()
weight_matrix(adata, l=1.2, cutoff=0.2, single_cell=False)  # weight_matrix by rbf kernel
extract_lr(adata, 'human', min_cell=3)
spatialdm_global(adata,1000, specified_ind=None, method='both', nproc=1)     # global Moran selection
sig_pairs(adata, method='permutation', fdr=True, threshold=0.1)
spatialdm_local(adata, n_perm=1000, method='both', specified_ind=None, nproc=1)     # local spot selection
sig_spots(adata, method='permutation', fdr=False, threshold=0.1)     # significant local spots

# print('done')
# data=["A1",
#       "A2",
#       "A8",
#       "A9"]
#
# A1_adata = dataset.A1()
# # A2_adata = dataset.A2()
# # A8_adata = dataset.A8()
# # A9_adata = dataset.A9()
# #
# createVar = locals()
# for d in data:
#     adata = locals()[d+'_adata']
#     weight_matrix(adata, l=75, cutoff=0.2, single_cell=False)  # weight_matrix by rbf kernel
#
#     extract_lr(adata,'human', min_cell=10)  # find overlapping LRs from CellChatDB
#
#     spatialdm_global(adata,method='z-score', nproc=1)  # global Moran selection
#
#     sig_pairs(adata,method='z-score', fdr=True, threshold=0.1)  # select significant pairs
#
#     spatialdm_local(adata,method='z-score', specified_ind=None, nproc=1)  # local spot selection
#     sig_spots(adata,method='z-score', fdr=False, threshold=0.1)  # significant local spots
#     createVar[d] = adata
#     print(d + ' done!')
# #
# # samples = [A1,A2, A8,A9]
# # concat=concat_obj(samples, data, 'human', 'z-score', fdr=False)
# # drop_uns_na(concat)
# # concat.write('concat.h5ad')
# concat = ann.read('concat.h5ad')
# import seaborn as sns
# conditions = np.hstack((np.repeat([1],2), np.repeat([0],2)))
# subset = ['A1', 'A2', 'A8', 'A9']
# differential_test(concat, subset, conditions)
# pl.differential_dendrogram(concat)
# group_differential_pairs(concat, 'adult', 'fetus')
# pl.differential_volcano(concat, legend=['adult specific', 'fetus specific'])
# print('done')