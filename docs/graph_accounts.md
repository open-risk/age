Some correspondences to make graph-based accounting more tangible

## Debits and Credits

Double-entry bookkeeping traditionally names movements of value (money) between accounts as *debits* or *credits*. As a form of validation, debits must exactly balance credits, both within an individual transaction and over all transactions.

In the graph representation via an incidence matrix this balance is *automatic*. A transaction is a graph edge between two accounts (nodes). The (single) numerical weight attached to the edge is a debit for one account and a credit for the other.

## Positive and Negative Numbers

We use positive and negative signs in the incidence matrix (instead of the debit and credit names). When value *leaves* an account it is a negative (credit). When value *reaches* an account it is a positive (debit). 

## Assets, Liabilities and Equity

An important set of accounts describe the state of an entity. They are stock accounts, they have a specific value at a given point in time. It is customary to segment stock accounts (graph nodes) by their fundamental characteristics. Those are determined by what kind of transactions these accounts are typically involved in. 

* Assets - Things owned, expected to provide utility, generate value
* Liabilities - Things owed, expected to extract value
* Equity - A special type of liability, the residual value attributable to the owners of the entity

In graph context this classification attaches labels to nodes. In turn, we use these labels to determine whether a transaction (an edge between nodes) is *allowable*.

## Revenue and Expenses

Another set of accounts has different profile: they capture the changes to stock accounts and are called flow accounts. They are defined as aggregates of transactions over a given period (rather than a fixed point in time). 

Two such amounts that are used to describe changes:

* Revenue - Value (money) flowing in
* Expenses - Value (money) flowing out

## Chart of Accounts

The three Asset, Liability and Equity accounts are very high-level (aggregated). 

Accounting subdivides into Taxonomies, Items and Line Items, effectively subaccounts, subsubaccounts, etc. This corresponds to a hierarchical graph node labeling scheme. E.g. assets can be subdivided into cash, real estate, inventory, equipment etc. Liabilities can be subdivided into different types of loans, trade finance, tax liabilities etc. Even equity can be subdivided into different forms.

Correspondingly, transactions (edges between accounts) can be labelled to denote summaries of specific categories. The totality of this classification scheme is called the chart of accounts. 