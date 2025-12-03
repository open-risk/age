# AGE is an Accounting Graph Environment

The project explores the representation of various accounting concepts using graph theory. 

## Background reading

The theoretical concepts underpinning the AGE code structure and functionality are documented in a number of white papers which are available in the *docs* directory.

* [WP19](docs/OpenRiskWP19_111125.pdf)


## About Accounting Graphs

Accounting graphs are mathematical representations of accounting using the tools of graph theory.

## Double-entry graphs

DEB graphs are representations of classic double entry accounting. E.g the classic balance sheet:

![Balance Sheet](images/balance.png)

The core tool towards DEB graph representation is to express accounts and transactions as nodes and edges for an *incidence matrix*. There are two main forms of this matrix, the direct and *reified* version.

![Balance Vectors](images/balance_vectors.png)

In both versions, each column of the matrix is a *balance vector* that sums to zero. For example a borrowing transaction would be represented as follows:

![DEB Graphs](images/borrowing.png)


## Quadruple-entry graphs

The graph framework can be extended to accommodate multiple accounting entities that engage in transactions (and keep separate books). 

The incidence matrix has a block structure that compiles transactions both within and across different entities.

![QEB Table](images/qeb_table.png)

When multiple entities are present transactions are naturally split into the internal (within an entity's account) and external sets (linking two entities).

![QEB Graph](images/qeb_graph.png)

The incidence matrix representation offers a systematic way to mirror external transactions using internal edges and thus decompose the network into disjoint graphs (the opposite is generally not possible).

An arbitrary number of entities can be added.

![QEB Accounting](images/qeb_accounting_graph.png)