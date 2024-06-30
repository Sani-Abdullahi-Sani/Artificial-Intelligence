**Prolog Programming Task**

*Introduction*
In this Task, we try to solve problems using Prolog, a logic programming language. Prolog is unique in its approach to problem-solving, emphasizing facts, rules, and logical inference. You can use SWI-Prolog, available for download on various operating systems, or the online interpreter that we used at [SWISH Online Prolog Interpreter](https://swish.swi-prolog.org/).

**Tasks**

**1. Family Tree**
We create a Prolog program to model a family tree. Define relationships such as parent, sibling, and grandparent using facts and rules. 

*Example facts include:*

- male(adam).
- female(eve).
- parent(adam, cain).

*And rules like:*

- father(X, Y) :- male(X), parent(X, Y).


**2. Logic Puzzle**
We Constructed a Prolog program to solve a logic puzzle with given constraints. Used rules to define relationships and constraints among different entities. For instance:

- rule1(C1, C2, C3, C4, C5) :- member(C, [C1, C2, C3, C4, C5]), C = [red, ntokozo, _, _, _, _].


**3. Graph Search**
We Implemented a depth-first search in a graph. Represent the graph with edge facts and define the path using rules. Example edge fact:

- edge(a, b).

*And the DFS rule:*

- path(X, Y, Path) :- dfs(X, Y, [X], Path).
