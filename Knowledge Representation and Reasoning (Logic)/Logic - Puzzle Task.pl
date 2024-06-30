% Logic Puzzle Task 
% Submitted By: 
% Sani Abdullahi Sani - 2770930

% Rule 1
rule1(C1,C2,C3,C4,C5):- member(C, [C1,C2,C3,C4,C5]), C = [red, ntokozo,_,_,_,_].

% Rule 2
rule2(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, saul, _, _, dog, _].

% Rule 3
rule3(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [green, _, coffee, _, _, _].

% Rule 4
rule4(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, kgosi, tea, _, _, _].

% Rule 5
rule5(C1,C2,C3,C4,C5) :-
   member(C, [C1,C2,C3,C4,C5]), C = [white, _, _, _, _, Pos1],
    member(R, [C1,C2,C3,C4,C5]), R = [green, _, _, _, _, Pos2],
    Pos2 is Pos1 + 1.

% Rule 6
rule6(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, _, _, superman, snails, _].

% Rule 7
rule7(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [yellow, _, _, hulk, _, _].

% Rule 8
rule8(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, _, milk, _, _, 3].

% Rule 9
rule9(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, jay, _, _, _, 1].

% Rule 10
rule10(C1,C2,C3,C4,C5) :-
    member(C, [C1,C2,C3,C4,C5]), C = [_, _, _, ironman, _, Pos1],
    member(R, [C1,C2,C3,C4,C5]), R = [_, _, _, _, parrot, Pos2],
    abs(Pos1 - Pos2) =:= 1.

% Rule 11
rule11(C1,C2,C3,C4,C5) :-
    member(C, [C1,C2,C3,C4,C5]), C = [_, _, _, hulk, _, Pos1],
    member(R, [C1,C2,C3,C4,C5]),  R = [_, _, _, _, horse, Pos2],
    abs(Pos1 - Pos2) =:= 1.

% Rule 12
rule12(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, _, orange, spiderman, _, _].

% Rule 13
rule13(C1,C2,C3,C4,C5) :- member(C, [C1,C2,C3,C4,C5]), C = [_, john, _, batman, _, _].

% Rule 14
rule14(C1,C2,C3,C4,C5) :-
    member(C, [C1,C2,C3,C4,C5]), C = [blue, _, _, _, _, Pos1],
    member(R, [C1,C2,C3,C4,C5]),  R = [_, jay, _, _, _, Pos2],
	abs(Pos1 - Pos2) =:= 1.

members([], _).
members([H|T], List) :-
    member(H, List),
    members(T, List).


% Solving the Puzzle
solve(C1,C2,C3,C4,C5) :-
C1 = [C1_col,C1_name,C1_drink,C1_superhero,C1_pet,1],
C2 = [C2_col,C2_name,C2_drink,C2_superhero,C2_pet,2],
C3 = [C3_col,C3_name,C3_drink,C3_superhero,C3_pet,3],
C4 = [C4_col,C4_name,C4_drink,C4_superhero,C4_pet,4],
C5 = [C5_col,C5_name,C5_drink,C5_superhero,C5_pet,5],
rule1(C1,C2,C3,C4,C5),
rule2(C1,C2,C3,C4,C5),
rule3(C1,C2,C3,C4,C5),
rule4(C1,C2,C3,C4,C5),
rule5(C1,C2,C3,C4,C5),
rule6(C1,C2,C3,C4,C5),
rule7(C1,C2,C3,C4,C5),
rule8(C1,C2,C3,C4,C5),    
rule9(C1,C2,C3,C4,C5), 
rule10(C1,C2,C3,C4,C5),
rule11(C1,C2,C3,C4,C5),
rule12(C1,C2,C3,C4,C5),
rule13(C1,C2,C3,C4,C5),
rule14(C1,C2,C3,C4,C5),
    
members([white, green, red, blue, yellow],
[C1_col,C2_col,C3_col,C4_col,C5_col]),
members([saul, john, ntokozo, kgosi, jay],
[C1_name,C2_name,C3_name,C4_name,C5_name]),
members([orange, coffee, milk, tea, water],
[C1_drink,C2_drink,C3_drink,C4_drink,C5_drink]),
members([spiderman, batman, superman, ironman, hulk],
[C1_superhero,C2_superhero,C3_superhero,C4_superhero,C5_superhero]),
members([dog, cat, snails, horse, parrot],
[C1_pet,C2_pet,C3_pet,C4_pet,C5_pet]).

