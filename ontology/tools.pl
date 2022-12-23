% tool profile , list of requirements
profile(nmap_1, [ip=IP]) :- ip(IP).

profile(hydra_ssh, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'ssh').
profile(hydra_telnet, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'telnet').
profile(hydra_ftp, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'ftp').

profile(gobuster_https, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'https').
profile(gobuster_http, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'http').


nmap_1(Parameters) :-
    format('nmap -F ~w',[Parameters.ip]).

hydra_ssh(Parameters) :-
    format('hydra -C wordlists/default_credentials/test.txt ~w ssh',[Parameters.ip]).

tools :-
    profile(Tool, Parameters),
    call(Tool, Parameters).