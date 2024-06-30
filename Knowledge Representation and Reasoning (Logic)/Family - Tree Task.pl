% 4.1: Facts
male(greg).
male(adam).
male(trent).
male(martin).
male(marcus).
male(gabriel).
male(dave).
male(michael).

female(lucy).
female(amy).
female(kgomotso).
female(naledi).
female(karen).
female(michelle).

% Parent-child relationships
parent(trent, greg).
parent(naledi, greg).
parent(trent, adam).
parent(trent, kgomotso).
parent(karen, adam).
parent(karen, kgomotso).
parent(gabriel, marcus).
parent(gabriel, michelle).
parent(gabriel, naledi).
parent(amy, marcus).
parent(amy, michelle).
parent(amy, naledi).
parent(dave, trent).
parent(dave, martin).
parent(lucy, trent).
parent(lucy, martin).
parent(martin, michael).

% Marriage relationships
married(amy, gabriel).
married(lucy, dave).
married(naledi, trent).


% 4.2: Rules

% Spouse relationship
spouse(X, Y) :- married(X, Y); married(Y, X).

% Mother relationship
mother(X, Y) :- parent(X, Y), female(X).

% Father relationship
father(X, Y) :- parent(X, Y), male(X).

% Sibling relationship
sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y.

% Brother relationship
brother(X, Y) :-
    sibling(X, Y),
    male(X).

% Sister relationship
sister(X, Y) :-
    sibling(X, Y),
    female(X).


% Half sibling relationship
half_sibling(X, Y) :-
    parent(Z, X),
    parent(W, Y),
    Z \= W,
    (father(Z, X), father(W, Y); mother(Z, X), mother(W, Y)).

% Half brother relationship
half_brother(X, Y) :-
    half_sibling(X, Y),
    male(X).

% Half sister relationship
half_sister(X, Y) :-
    half_sibling(X, Y),
    female(X).

% Uncle relationship
uncle(X, Y) :-
    (father(Z, Y); mother(Z, Y)),
    brother(X, Z).

% Aunt relationship
aunt(X, Y) :-
    (father(Z, Y); mother(Z, Y)),
    sister(X, Z).

% Grandparent relationship
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

% Grandmother relationship
grandmother(X, Y) :-
    grandparent(X, Y),
    female(X).

% Grandfather relationship
grandfather(X, Y) :-
    grandparent(X, Y),
    male(X).

% Nephew relationship
nephew(X, Y) :-
    (aunt(Y, X); uncle(Y, X)),
    male(X).

% Niece relationship
niece(X, Y) :-
    (aunt(Y, X); uncle(Y, X)),
    female(X).

% Cousin relationship
cousin(X, Y) :-
    (parent(Z, X); parent(W, Y)),
    sibling(Z, W).

% In-law relationship
in_law(X, Y) :-
    spouse(X, Z),
    (sibling(Z, Y); sibling(Y, Z); parent(Z, Y); parent(Y, Z)).

% Brother-in-law relationship
brother_in_law(X, Y) :-
    in_law(X, Y),
    male(X).

% Sister-in-law relationship
sister_in_law(X, Y) :-
    in_law(X, Y),
    female(X).
