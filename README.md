# mSing

Implementation of Multifractal Detrended Fluctuation Analysis for Multidimensional data (1D+1,2D+1,3D+1,4D+1,...)  based on [LRydin's code](https://github.com/LRydin/MFDFA).

## Instalation

    pip install git+https://github.com/rsautter/mSing/

## Usage
    import mSing
    import matplotlib.pyplot as plt
    import numpy as np

    wn = np.random.rand(256,256)
    q=np.linspace(-0.5,0.5,100)
    a, fa = mSing.mSing(wn, np.linspace(8,32,10), q)
    plt.figure()
    plt.plot(a, fa, 'o-')
    plt.xlabel('a')
    plt.ylabel('f(a)')
    plt.title('Singularity Spectrum')  
    plt.grid()
    plt.show()

## Details
  1. Uses Multidimensional Fast Fourier Transform (FFT) for detecting DFA trends.
  2. Series Profile is given at every dimension in sequence.
  3. Space is recursively divided into equal-size time series, matrices, or hypercubes.

## Examples
  Notebooks with examples are provided in notebooks/ folder.
