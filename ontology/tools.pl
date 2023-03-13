tools(Tool, Profile, Command) :-
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

tools_duration(Tool, Profile, Command) :-
    findall(P, profile(P, _), Profiles),
    getLowest(Profiles, Profile, _),
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

tools_score(Tool, Profile, Command) :-
    findall(P, profile(P, _), Profiles),
    getHighest(Profiles, Profile, _),
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

getLowest([], _, 9999999).
getLowest([H|T], Profile, Min) :-
    avgProfileDuration(H, Avg),
    getLowest(T, NewProfile, Min1),
    (Avg < Min1 -> (Min = Avg, Profile = H) ; (Min = Min1, Profile = NewProfile)).


getHighest([], _, -1).
getHighest([H|T], Profile, Max) :-
    avgProfileScore(H, Avg),
    getHighest(T, NewProfile, Max1),
    (Avg > Max1 -> (Max = Avg, Profile = H) ; (Max = Max1, Profile = NewProfile)).

format_command(Template, Parameters, Command) :-
    format(string(Command), Template, Parameters).