:- consult(parser).
:- consult(tools_config).

tools(Tool, Profile, Command) :-
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile),
    assertz(executed(Profile, Command)).

tools_duration(Tool, Profile, Command) :-
    findall(P, profile(P, _), Profiles),
    getLowest(Profiles, Profile, _),
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile),
    assertz(executed(Profile, Command)).

tools_score(Tool, Profile, Command) :-
    findall(P, profile(P, _), Profiles),
    getHighest(Profiles, Profile, _),
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile),
    assertz(executed(Profile, Command)).

adjust_ProfileScore(Profile, Score) :-
    simular_tools_executed(Profile, X),
    avgProfileScore(Profile, Avg),
    get_time(Now),
    latestProfileExecution(Profile, Last_execution),
    Score is Avg - X + ((Now - Last_execution)/1000).


simular_tools_executed(Profile, X) :-
    bagof(P, executed(P), Profiles) -> has_same_results(Profile, Profiles, X); X = 0.

has_same_results(Profile, Executed_profiles, X) :-
    profileResults(Profile, Results),
    has_same_results_helper(Results, Executed_profiles, 0, X).

has_same_results_helper(_, [], Acc, Acc).
has_same_results_helper(Results, [Executed_profile | Executed_profiles], Acc, X) :-
    profileResults(Executed_profile, Executed_results),
    (test_X(Results, Executed_results) ->
        Acc1 is Acc + 1,
        has_same_results_helper(Results, Executed_profiles, Acc1, X) ;
        has_same_results_helper(Results, Executed_profiles, Acc, X)).


test_X([], _).
test_X([X | Xs], Ys) :-
    memberCheckSimple(Ys,X),
    test_X(Xs, Ys).


% https://stackoverflow.com/questions/40530172/check-if-an-element-is-member-of-a-list
memberCheckSimple([H|T], H).
memberCheckSimple([_|T], H) :- memberCheckSimple(T, H).

getLowest([], _, 9999999).
getLowest([H|T], Profile, Min) :-
    avgProfileDuration(H, Avg),
    getLowest(T, NewProfile, Min1),
    (Avg < Min1 -> (Min = Avg, Profile = H) ; (Min = Min1, Profile = NewProfile)).


getHighest([], _, -1).
getHighest([H|T], Profile, Max) :-
    adjust_ProfileScore(H, Score),
    getHighest(T, NewProfile, Max1),
    (Score > Max1 -> (Max = Score, Profile = H) ; (Max = Max1, Profile = NewProfile)).

format_command(Template, Parameters, Command) :-
    format(string(Command), Template, Parameters).