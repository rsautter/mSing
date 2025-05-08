# This code is an adaptation of LRydin's work (https://github.com/LRydin/MFDFA) for multidimensional systems
# We apply the Fourier transform to detect trends

import numpy as np
from .singspect import singularity_spectrum
from typing import Tuple


__all__ = [
    'mSing',
    'splitBlock',
    'ftTrend'
]

def splitBlock(mat,window=2,dim=0,step=1):
  out = []
  s = mat.shape
  for i in range(0,s[dim]-window,step):
    if dim<len(s)-1:
      temp = np.swapaxes(mat,0,dim)[i:i+window]
      temp = np.swapaxes(temp,dim,0)
      blocks = splitBlock(temp,window,dim+1,step)
      for b in blocks:
        out.append(b)
    else:
      temp = np.swapaxes(mat,0,dim)[i:i+window]
      temp = np.swapaxes(temp,dim,0)
      out.append(np.array(temp))
  return out
  
def ftTrend(mat, tol=1e-3):
    ft = np.fft.fftn(mat)
    freq_grids = np.meshgrid(*[np.fft.fftfreq(n) for n in mat.shape], indexing='ij')
    freq_magnitude = np.sqrt(sum(f**2 for f in freq_grids))
    ft[freq_magnitude > tol] = 0
    return np.real(np.fft.ifftn(ft))
  
def qdfa(timeseries: np.ndarray, lag: np.ndarray,q: np.ndarray = 2) -> Tuple[np.array, np.ndarray]:

    # Force lag to be ints, ensure lag > order + 1
    lag = lag[lag > 2]
    lag = np.round(lag).astype(int)

    # Size of array
    shape = timeseries.shape

    # Fractal powers as floats
    q = np.asarray_chkfinite(q, dtype=float)

    # Ensure q≈0 is removed, since it does not converge. Limit set at |q| < 0.1
    q = q[(q < -.1) + (q > .1)]

    # Reshape q to perform np.float_power
    q = q.reshape(-1, 1)

    # "Profile" of the series
    Y = np.cumsum(timeseries - np.mean(timeseries,axis=0))
    for i in range(1,len(Y.shape)):
      Y = np.cumsum(Y - np.mean(Y,axis=i))

    # Return f of (fractal)-variances
    f = np.empty((lag.size, q.size))

    for li,i in enumerate(lag):
        blocks = splitBlock(Y,i,step=i)
        F = np.empty(len(blocks))
        ub = []
        for bi,b in enumerate(blocks):
            ub.append(np.var((b-ftTrend(b)).reshape(-1)))

        F_q = []
        for q_i in q:
            if np.isclose(q_i, 0.0):
              F_q.append(np.exp(0.5 * np.mean(np.log(ub))))
            else:
              F_q.append(np.power(np.mean(np.power(ub, q_i / 2.0)), 1.0 / q_i))
        f[li] = np.array(F_q).reshape(-1)
    return lag, f

def mSing(timeseries: np.ndarray, lag: np.ndarray,q: np.ndarray = 2) -> Tuple[np.array, np.ndarray]:
    '''
    Returns 
        alpha, falpha
    '''
    lag,f = qdfa(timeseries,lag, q)
    return singularity_spectrum(lag,f,q)
