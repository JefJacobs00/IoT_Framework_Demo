tools(Tool, Profile, Command) :-
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

test(Profiles) :-
    findall(Profile, profile(Profile, Parameters), Profiles),
    do(Profiles).

do([]).
do([H|T]) :-
    write(H),
    avgProfileDuration(H, Avg),
    write(Avg),
    do(T).

tools_duration(Tool, Profile, Command) :-
    lowest_duration(Profile, Duration),
    tools(Tool, Profile, Command).

lowest_duration(Profile, Min) :-
    findall(Avg, avgProfileDuration(Profile, Avg), Averages),
    list_min(Averages, Min),
     avgProfileDuration(Profile, Min).

format_command(Template, Parameters, Command) :-
    format(string(Command), Template, Parameters).

list_min([L|Ls], Min) :-
    list_min(Ls, L, Min).

list_min([], Min, Min).
list_min([L|Ls], Min0, Min) :-
    Min1 is min(L, Min0),
    list_min(Ls, Min1, Min).