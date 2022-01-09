#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
==================
Statistics Helpers
==================

:Author:
    Moritz Emanuel Beber
:Date:
    2011-01-23
:Copyright:
    Copyright(c) 2011 Jacobs University of Bremen. All rights reserved.
:File:
    statistics.py
"""


import numpy
import numpy.ma as nma
import scipy
import scipy.stats

from operator import itemgetter


def probability_bincount(obs, drop=True):
    """
    Normalise the observed bincount from `obs` to sum up to unity.

    Parameters
    ----------
    obs: iterable
        An iterable of integer numerals.
    drop: bool (optional)
        Determines whether or not bins with zero events are dropped from the
        resulting list.

    Returns
    -------
    A frequency distribution that is normalised to unity.
    """
    obs = nma.asanyarray(obs, dtype="int32")
    nma.masked_invalid(obs, copy=False)
    obs = numpy.ravel(obs)
    if obs.size == 0:
        return list()
    total = float(len(obs))
    freq = numpy.bincount(obs[~obs.mask])
    points = [(k, val / total) for (k, val) in enumerate(freq) if val > 0]
    return points

def frequency_distribution(obs, num_bins=30, binwidth=None, limits=None,
        weights=None, drop=True):
    """
    Takes a number of events and counts the frequency of these events falling into
    either a fixed number of equi-distant bins over the given range or bins of
    fixed width over the range.

    Parameters
    ----------
    obs: iterable
        An aggregation of numerical observations.
    num_bins: int (optional)
        The number of equi-distant bins used over the numeric range.
    binwidth: float (optional)
        Desired width of the bins. This overrides `num_bins`.
    limits: tuple (lower, upper) (optional)
        The lower and upper values for the range of the distribution.
        If no value is given, a range slightly larger then the range of the
        values in `obs` is used. Specifically ``(a.min() - s, a.max() + s)``,
            where ``s = (1/2)(a.max() - a.min()) / num_bins``.
    weights: iterable (optional)
        Weights for the data points in `obs`. The default is `None` weighting
        all points equal.
    drop: bool (optional)
        Determines whether or not bins with zero events are dropped from the
        resulting list.

    Returns
    -------
    A list of pairs, the first entry is the centre of the bin borders at which
    the frequency of an event is measured, and the second entry is the frequency
    itself.
    """
    obs = nma.asanyarray(obs)
    nma.masked_invalid(obs, copy=False)
    obs = numpy.ravel(obs)
    if obs.size == 0:
        return list()
    if limits is None:
        mn = obs.min()
        mx = obs.max()
    else:
        (mn, mx) = limits
    if binwidth:
        binwidth = float(binwidth)
        num_bins = numpy.floor((mx - mn) / binwidth)
    else:
        num_bins = int(num_bins)
        binwidth = (mx - mn) / num_bins
    offset = binwidth * 0.5
    if limits is None:
        limits = (mn - offset, mx + offset)
    # extend the numeric range slightly beyond the data range
    (freq, bins) = numpy.histogram(obs[~obs.mask], bins=num_bins, range=limits,
            weights=weights)
    if drop:
        points = [(bins[k] + offset, freq[k]) for k in range(freq.size)\
                if freq[k] > 0]
    else:
        points = [(bins[k] + offset, freq[k]) for k in range(freq.size)]
    return points

def probability_distribution(obs, num_bins=30, binwidth=None, limits=None,
        weights=None, drop=True):
    """
    Normalises the observed frequencies in `obs` by the total number of elements in
    `obs` making this a probability mass function.

    Parameters
    ----------
    obs: iterable
        An aggregation of numerical observations.
    num_bins: int (optional)
        The number of equi-distant bins used over the numeric range.
    binwidth: float (optional)
        Desired width of the bins. This overrides `num_bins`.
    limits: tuple (lower, upper) (optional)
        The lower and upper values for the range of the distribution.
        If no value is given, a range slightly larger then the range of the
        values in `obs` is used. Specifically ``(a.min() - s, a.max() + s)``,
            where ``s = (1/2)(a.max() - a.min()) / num_bins``.
    weights: iterable (optional)
        Weights for the data points in `obs`. The default is `None` weighting
        all points equal.
    drop: bool (optional)
        Determines whether or not bins with zero events are dropped from the
        resulting list.

    Returns
    -------
    A frequency distribution whose sum is normalised to unity.

    Notes
    -----
    See also frequency_distribution_.
    """
    points = frequency_distribution(obs, num_bins, binwidth, limits, weights, drop)
    freq = itemgetter(1)
    total = float(sum(freq(val) for val in points))
    return [(pair[0], pair[1] / total) for pair in points]

def adaptive_distribution(obs, binwidth, limits=None, factor=2.0, k_max=21, right_most=3):
    """
    An adaptive binning technique that overlays multiple histograms with
    increasing bin widths.

    References
    ----------
    [1] Liebovitch, L. S., A. T. Todorov, M. Zochowski, D. Scheurle, L. Colgin,
        M. A. Wood, K. A. Ellenbogen, J. M. Herre, and R. C. Bernstein. 1999.
        ``Nonlinear Properties of Cardiac Rhythm Abnormalities.''
        Physical Review E 59 (3): 3312–3319.

    """
    obs = nma.asanyarray(obs)
    nma.masked_invalid(obs, copy=False)
    obs = numpy.ravel(obs)
    if obs.size == 0:
        return list()
    if limits is None:
        mn = obs.min()
        mx = obs.max()
    else:
        (mn, mx) = limits
    offset = binwidth * 0.5
    if limits is None:
        limits = (mn - offset, mx + offset)
    num_bins = numpy.floor((mx - mn) / binwidth)
    freq = numpy.histogram(obs[~obs.mask], num_bins, range=limits)[0]
    total = float(freq.sum())
    print(0)
    print(binwidth)
    print(freq[0:right_most + 1])
    results = list()
    iteration = 1
    while len(freq) > right_most and not (freq[1:right_most] == 0).any():
        for (k, count) in enumerate(freq[1:]):
            if count == 0 or k == k_max:
                break
            results.append(((k + 0.5) * binwidth + limits[0], count / (binwidth * total)))
        binwidth *= factor
        iteration += 1
        # new loop
        num_bins = numpy.floor((mx - mn) / binwidth)
        freq = numpy.histogram(obs, num_bins, range=limits)[0]
        total = float(freq.sum())
        print(iteration)
        print(binwidth)
        print(freq[0:right_most + 1])

    return sorted(results)

def compute_zscore(obs, random_stats):
    """
    Parameters
    ----------
    obs: numeral
        original observation
    random_stats : iterable
        same observable in randomised versions
    """
    random_stats = nma.asanyarray(random_stats)
    nma.masked_invalid(random_stats, copy=False)
    random_stats = numpy.ravel(random_stats)
    if random_stats.size == 0:
        return numpy.nan
    mean = numpy.mean(random_stats.filled(0.0))
    std = numpy.std(random_stats.filled(0.0))
    nominator = obs- mean
    if nominator == 0.0:
        return nominator
    if std == 0.0:
        if nominator < 0.0:
            return -numpy.inf
        else:
            return numpy.inf
    else:
        return (nominator / std)

def dense_ranking(data, dtype="int32"):
    """
    Ranks the given data in increasing order with duplicates receiving the same
    rank and ranking continuously, i.e.,

        [0.5, 1.2, 3.4, 1.2, 1.2] -> [1, 2, 3, 2, 2].

    Parameters
    ----------
    data: numpy.array
        data to be ranked, should behave like a numpy.array
    dtype: str (optional)
        string desciribing the data type of the numpy.array storing the ranks

    Returns
    -------
    numpy.array:
        ranks of the data as explained above

    Notes
    -----
    The given data should be one-dimensional. This can be achieved using
    numpy.ravel and then reshaping the result as necessary.

    If the data contains `nan` or other undesirable values, masked arrays may be
    your solution.
    """
    # numpy.unique returns the unique values in sorted order
    (unique, indices) = numpy.unique(data, return_inverse=True)
    # use the returned indices over a range to construct ranked array
    ranks = numpy.arange(1, unique.size + 1)[indices].astype(dtype)
    return ranks

def competition_ranking(data, dtype="int32"):
    """
    Ranks the given data in increasing order and resolving duplicates using the
    lowest common rank and skipping as many ranks as there are duplicates, i.e.,

        [0.5, 1.2, 3.4, 1.2, 1.2] -> [1, 2, 5, 2, 2].

    Parameters
    ----------
    data: numpy.array
        data to be ranked, should behave like a numpy.array
    dtype: str (optional)
        string desciribing the data type of the numpy.array storing the ranks

    Returns
    -------
    numpy.array:
        ranks of the data as explained above

    Notes
    -----
    The given data should be one-dimensional. This can be achieved using
    numpy.ravel and then reshaping the result as necessary.

    If the data contains `nan` or other undesirable values, masked arrays may be
    your solution.
    """
    ranks = numpy.zeros(data.size, dtype=dtype)
    order = data.argsort()
    ranks[order] = numpy.arange(1, data.size + 1)
    # returns repeats and their count
    repeats = scipy.stats.mstats.find_repeats(data)[0]
    for r in repeats:
        condition = data == r
        # all repeats have the same minimal rank
        # using the first element works iff sorting was stable
#        ranks[condition] = ranks[condition][0]
        ranks[condition] = ranks[condition].min()
    return ranks

def modified_competition_ranking(data, dtype="int32"):
    """
    Ranks the given data in increasing order and resolving duplicates using the
    largest common rank and skipping as many ranks as there are duplicates, i.e.,

        [0.5, 1.2, 3.4, 1.2, 1.2] -> [1, 4, 5, 4, 4].

    Parameters
    ----------
    data: numpy.array
        data to be ranked, should behave like a numpy.array
    dtype: str (optional)
        string desciribing the data type of the numpy.array storing the ranks

    Returns
    -------
    numpy.array:
        ranks of the data as explained above

    Notes
    -----
    The given data should be one-dimensional. This can be achieved using
    numpy.ravel and then reshaping the result as necessary.

    If the data contains `nan` or other undesirable values, masked arrays may be
    your solution.
    """
    ranks = numpy.zeros(data.size, dtype=dtype)
    order = data.argsort()
    ranks[order] = numpy.arange(1, data.size + 1)
    # returns repeats and their count
    repeats = scipy.stats.mstats.find_repeats(data)[0]
    for r in repeats:
        condition = data == r
        # all repeats have the same minimal rank
        # using the first element works iff sorting was stable
#        ranks[condition] = ranks[condition][-1]
        ranks[condition] = ranks[condition].max()
    return ranks

