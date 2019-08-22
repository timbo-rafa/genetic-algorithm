[![Build Status](https://travis-ci.org/timbo-rafa/genetic-algorithm.svg?branch=master)](https://travis-ci.org/timbo-rafa/genetic-algorithm)

# Genetic Algorithm
Genetic Algorithm for the Traveling Salesman Problem

## Problem

#### Definition

Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the origin city?
It is an NP-hard problem in combinatorial optimization.

#### Data Modeling

The TSP can be modelled as an undirected weighted graph, such that cities are the graph's vertices, paths are the graph's edges, and a path's distance is the edge's weight.
It is a minimization problem starting and finishing at a specified vertex
after having visited each other vertex exactly once.

#### Solution Technique

Genetic algorithms are evolutionary techniques used for optimization purposes according to survival of the fittest idea. These methods do not ensure optimal solutions; however, they give good approximation usually in time. The genetic algorithms are useful for NP-hard problems, especially the traveling salesman problem. We used this technique here.

## Installation

```bash
git clone https://github.com/timbo-rafa/genetic-algorithm
cd genetic-algorithm
pip install networkx
```

## Running

![Running](https://raw.githubusercontent.com/timbo-rafa/genetic-algorithm/master/screenshots/genetic-algorithms-run.gif)

### Testing

Tests made using [nose](http://nose.readthedocs.io/en/latest/)
![Testing](https://raw.githubusercontent.com/timbo-rafa/genetic-algorithm/master/screenshots/genetic-algorithms-test.gif)

### Profiling

![Profiling](https://raw.githubusercontent.com/timbo-rafa/genetic-algorithm/master/screenshots/genetic-algorithms-profiler.gif)
