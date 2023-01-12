#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
==================
Network Algorithms
==================

:Author:
    Moritz Emanuel Beber
:Date:
    2011-03-07
:Copyright:
    Copyright(c) 2011 Jacobs University of Bremen. All rights reserved.
:File:
    algorithms.py
"""


import random
import itertools
import numpy
import networkx as nx
import statistics as stats


def graph_symmetries(graph):
    """
    Finds all symmetries of a graph. This is computationally very expensive
    O(N!) where N is the number of nodes in graph.
    """
    permutations = [dict(list(zip(graph.nodes_iter(), perm))) for perm in
            itertools.permutations(graph.nodes_iter())]
    keys = subgraph.nodes()
    keys.sort()
    symmetries = [[perm[node] for node in keys] for perm in permutations if
            all(graph.has_edge(perm[src], perm[tar])
            for (src, tar) in graph.edges_iter())]
    return symmetries

def spectral_community_detection(graph, weighted=True, threshold=1E-05,
                                 error_margin=100, refine=True,
                                 max_iter=500, binary_split=False):
    """
    Finds communities in a graph via spectral partitioning.

    Requires a graph whose nodes are integers from 0 to (number of nodes - 1).
    """
    dot = numpy.dot
    norm = numpy.linalg.norm
    ix = numpy.ix_
    kronecker = numpy.kron
    array = numpy.array
    zeros = numpy.zeros
    error_margin = error_margin * numpy.finfo(float).eps

    def _delta_modularity(s, b, m):
        res = dot(dot(s, b), s) / m
        return res[0, 0]

    def _kernighan_lin(s, b):
        def flip(v, pos):
            newv = v.copy()
            newv[pos] = -1 * v[pos]
            return newv
        def dq(s2):
            return dot(dot(s2,b),s2)
        s_best = s
        d_q_best = dq(s_best)
        while True:
            trials = [dq(flip(s_best, i)) for i in range(len(s_best))]
            if max(trials) > d_q_best:
                i = trials.index(max(trials))
                s_best = flip(s_best, i)
                d_q_best = dq(s_best)
            else:
                break
        return s_best

    def _split(nbunch):
        len_nodes = len(nbunch)
        # use the relevant subpart of the modularity matrix
        sub_b = b[ix(nbunch, nbunch)]
        for i in range(len_nodes):
            sub_b[i, i] -= sub_b[i, :].sum()
        # eigenvalues, eigenvectors
        (w, v) = numpy.linalg.eigh(sub_b)
        i = w.argmax()
        # convert to sign vector as defined on pg. 8579
        s = array([(1 if x > 0 else -1) for x in v[:, i]])
#        # find the dominant eigenvector by power method as in eq. 7
#        vec_old = zeros(len_nodes)
#        vec_new = array([random.random() for i in range(len_nodes)])
#        for i in range(max_iter):
#            vec_old = vec_new
##            vec_new = dot(sub_adj.A, vec_old) - (dot(deg, dot(deg, vec_old)) / m2)
#            vec_new = dot(sub_b.A, vec_old)
#            vec_new /= norm(vec_new)
#            if abs(vec_new - vec_old).sum() < threshold:
#                break
#        # convert to sign vector as defined on pg. 8579
#        s = array([(1 if x > 0 else -1) for x in vec_new])
        # dQ as in eq. 2 and 5
        d_q = _delta_modularity(s, sub_b, m4)
        if d_q <= error_margin:
            return False
        if refine:
            s = _kernighan_lin(s, sub_b)
            d_q = _delta_modularity(s, sub_b, m4)
        spectral_community_detection.modularity += d_q
        group1 = list()
        group2 = list()
        for (i, sign) in enumerate(s):
            if sign < 0:
                group1.append(nbunch[i])
            else:
                group2.append(nbunch[i])
        return [group1, group2]

    if graph.is_directed():
        raise nx.NetworkXError("only undirected graphs are allowed")
    # construct adjacency matrix
    adj = nx.to_numpy_matrix(graph)
    n = graph.order()
    m2 = graph.size() * 2.0
    m4 = m2 * 2.0
    # store the degree of each node in an array at corresponding index
    nbunch = sorted(graph.nodes())
    degrees = array([adj[i, :].sum() for i in nbunch])
    # construct modularity matrix
    b = adj - (kronecker(degrees, degrees) / m2).reshape(n, n)
    # initialize algorithm
    communities = list()
    spectral_community_detection.modularity = 0.0
    partitions = list()
    partitions.append(nbunch)
    successful_split = False
    ctr = 0
    print('Entering while loop')
    while partitions and ((not binary_split) or (not successful_split)):
        nbunch = partitions.pop(0)
        if not nbunch:
            continue
        groups = _split(nbunch)
        if not groups:
            communities.append(nbunch)
        else:
            ctr += 1
            print(ctr, 'partitions')
            successful_split = True
            partitions.extend(groups)
    if binary_split:
        communities.extend(partitions)
    return (spectral_community_detection.modularity, communities)

