http(Ip) :- deviceSerices(Ip,literal('http')).
ssh(Ip) :- deviceSerices(Ip,literal('ssh')).
telnet(Ip) :- deviceSerices(Ip,literal('telnet')).
ftp(Ip) :- deviceSerices(Ip,literal('ftp')).

requirements(nmap, [ip]).

requirements(gobuster, [ip,http]).

requirements(hydra,[ip,ssh]). 
requirements(hydra,[ip,telnet]).
requirements(hydra,[ip,ftp]).



check_requirements([]).
check_requirements([Predicate|Predicates]) :-
    call(Predicate, X),  
    findall(X, call(Predicate, X), List), 
    List \= [], 
    check_requirements(Predicates).

check_tool_requirements(Tool) :-
    requirements(Tool, Requirements),
    check_requirements(Requirements).



all_requirements_satisfied(Tool,Device) :-
    requirements(Tool, Requirements),
    forall(member(Requirement, Requirements), satisfies_requirement(Device, Requirement)).
