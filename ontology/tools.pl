tools(Tool, Profile, Command) :-
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).

format_command(Template, Parameters, Command) :-
    format(string(Command), Template, Parameters).