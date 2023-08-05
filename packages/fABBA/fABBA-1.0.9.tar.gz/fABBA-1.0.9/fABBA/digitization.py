# License: BSD 3 clause

# Copyright (c) 2021, Stefan Güttel, Xinye Chen
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Digitization -- based on aggregation

import warnings

try:
    import scipy
    try:
        if scipy.__version__ <= '1.8.0':
            from .separate.aggregation_cm import aggregate as aggregate_fc 
        else:
            from .separate.aggregation_c import aggregate as aggregate_fc 
        
        # cython with memory view
        from .extmod.fabba_agg_cm import aggregate as aggregate_fabba 
        
    except ModuleNotFoundError:
        from .separate.aggregation_c import aggregate as aggregate_fc 
        from .extmod.fabba_agg_c import aggregate as aggregate_fabba 
    

except (ModuleNotFoundError):
    from .separate.aggregation import aggregate as aggregate_fc 
    from .fabba_agg import aggregate as aggregate_fabba
    from .inverse_t import *
    
import collections
import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class Model:
    centers: np.ndarray # store aggregation centers
    splist: np.ndarray # store start point data

    hashm: dict # labels -> symbols, symbols -> labels
    
    
    
def digitize(pieces, alpha=0.5, sorting='norm', scl=1, alphabet_set=0):
    """
    Greedy 2D clustering of pieces (a Nx2 numpy array),
    using tolernce alpha and len/inc scaling parameter scl.
    A 'temporary' group center, which we call it starting point,
    is used  when assigning pieces to clusters. This temporary
    cluster is the first piece available after appropriate scaling 
    and sorting of all pieces. After finishing the grouping procedure,
    the centers are calculated the mean value of the objects within 
    the clusters

    Parameters
    ----------
    pieces - numpy.ndarray
        The compressed pieces of numpy.ndarray with shape (n_samples, n_features) after compression

    Returns
    ----------
    string (str or list)
        string sequence
    """
    
    pieces = np.array(pieces)[:,:2].astype(np.float64)
    
    if sorting not in ["lexi", "2-norm", "1-norm", "norm", "pca"]:
        raise ValueError("Please refer to a specific and correct sorting way, namely 'lexi', '2-norm' and '1-norm'")

    _std = np.std(pieces, axis=0) 

    if _std[0] != 0: # to prevent 0 std when assign max_len as 1 to compression, which make aggregation go wrong.
        npieces = pieces * np.array([scl, 1]) / _std
    else:
        npieces = pieces * np.array([scl, 1])
        npieces[:,1] = npieces[:,1] / _std[1]

    if sorting in ["lexi", "2-norm", "1-norm"]:
        # warnings.warn(f"Pass {sorting} as keyword args. From the next version "
        #      f"passing these as positional arguments "
        #      "will result in an error. Additionally, cython implementation will be impossible for this sorting.", 
        #              FutureWarning)
        labels, splist = aggregate_fabba(npieces, sorting, alpha)
    else:
        labels, splist = aggregate_fc(npieces, sorting, alpha)

    centers = np.zeros((0,2))

    for c in range(len(splist)):
        indc = np.argwhere(labels==c)
        center = np.mean(pieces[indc,:], axis=0)
        centers = np.r_[ centers, center ]

    string, hashm = symbolsAssign(labels, alphabet_set)

    parameters = Model(centers, np.array(splist), hashm)
    return string, parameters



def inverse_digitize(strings, parameters):
    """
    Convert symbolic representation back to compressed representation for reconstruction.

    Parameters
    ----------
    string - string
        Time series in symbolic representation using unicode characters starting
        with character 'a'.

    centers - numpy array
        centers of clusters from clustering algorithm. Each centre corresponds
        to character in string.

    Returns
    -------
    pieces - np.array
        Time series in compressed format. See compression.
    """

    pieces = np.empty([0,2])
    for p in strings:
        pc = parameters.centers[int(parameters.hashm[p])]
        pieces = np.vstack([pieces, pc])
    return pieces[:,0:2]



def calculate_group_centers(data, labels):
    agg_centers = list() 
    for c in set(labels):
        center = np.mean(data[labels==c,:], axis=0).tolist()
        agg_centers.append( center )
    return np.array(agg_centers)



def wcss(data, labels, centers):
    inertia_ = 0
    for i in np.unique(labels):
        c = centers[i]
        partition = data[labels == i]
        inertia_ = inertia_ + np.sum(np.linalg.norm(partition - c, ord=2, axis=1)**2)
    return inertia_





def symbolsAssign(clusters, alphabet_set=0):
    """
    Automatically assign symbols to different groups, start with '!'
    
    Parameters
    ----------
    clusters - list or pd.Series or array
        The list of labels.
            
    alphabet_set - int or list, default=0
        The list of alphabet letter. Here provide two different kinds of alphabet letters, namely 0 and 1.
        
    ----------
    Return:
    strings(list of string), hashmap(dict): repectively for the
    corresponding symbolic sequence and the hashmap for mapping from symbols to labels or 
    labels to symbols.
    """
    
    if alphabet_set == 0:
        alphabet = ['A','a','B','b','C','c','D','d','E','e',
                    'F','f','G','g','H','h','I','i','J','j',
                    'K','k','L','l','M','m','N','n','O','o',
                    'P','p','Q','q','R','r','S','s','T','t',
                    'U','u','V','v','W','w','X','x','Y','y','Z','z']
    
    elif alphabet_set == 1:
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    elif isinstance(alphabet_set, list) and len(alphabet):
        alphabet = alphabet_set
       
    else:
        raise ValueError('Please specify a legal parameter value for alphabet_set.')
    clusters = pd.Series(clusters)
    N = len(clusters.unique())

    cluster_sort = [0] * N 
    counter = collections.Counter(clusters)
    for ind, el in enumerate(counter.most_common()):
        cluster_sort[ind] = el[0]

    if N >= len(alphabet):
        alphabet = [chr(i+33) for i in range(0, N)]
    else:
        alphabet = alphabet[:N]
    hashm = dict(zip(cluster_sort + alphabet, alphabet + cluster_sort))
    strings = [hashm[i] for i in clusters]
    return strings, hashm




def quantize(pieces):
    """
    Realign window lengths with integer grid.

    Parameters
    ----------
    pieces: Time series in compressed representation.

    Returns
    -------
    pieces: Time series in compressed representation with window length adjusted to integer grid.
    """

    if len(pieces) == 1:
        pieces[0,0] = round(pieces[0,0])

    else:
        for p in range(len(pieces)-1):
            corr = round(pieces[p,0]) - pieces[p,0]
            pieces[p,0] = round(pieces[p,0] + corr)
            pieces[p+1,0] = pieces[p+1,0] - corr
            if pieces[p,0] == 0:
                pieces[p,0] = 1
                pieces[p+1,0] -= 1
        pieces[-1,0] = round(pieces[-1,0],0)

    return pieces
