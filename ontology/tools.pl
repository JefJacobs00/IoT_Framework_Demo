tools(Tool, Profile, Command) :-
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

tools_duration(Tool, Profile, Command) :-
    findall(P, profile(P, _), Profiles),
    getLowest(Profiles, Profile, Min),
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

getLowest([], _, 9999999).
getLowest([H|T], Profile, Min) :-
    avgProfileDuration(H, Avg),
    getLowest(T, NewProfile, Min1),
    (Avg < Min1 -> (Min = Avg, Profile = H) ; (Min = Min1, Profile = NewProfile)).

format_command(Template, Parameters, Command) :-
    format(string(Command), Template, Parameters).