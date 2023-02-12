tool(nmap, nmap_1).
tool(nmap, nmap_2).

tool(hydra, hydra_ssh).
tool(hydra, hydra_ftp).
tool(hydra, hydra_telnet).

tool(gobuster, gobuster_http).
tool(gobuster, gobuster_https).

profile(nmap_1, [ip=IP]) :- ip(IP).
profile(nmap_2, [ip=IP,port=P]) :- ip(IP), devicePorts(IP,P).

profile(hydra_ssh, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'ssh').
profile(hydra_telnet, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'telnet').
profile(hydra_ftp, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'ftp').

profile(gobuster_https, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'https').
profile(gobuster_http, [ip=IP, port=P]) :- ip(IP), deviceServices(IP, P, 'http').

format_command(Template, Parameters, Command) :-
    format(string(Command), Template, Parameters).

nmap_1(Parameters, Command) :-
    format_command('nmap -F ~w', [Parameters.ip], Command).

nmap_2(Parameters, Command) :-
    format_command('nmap -sC -sV -p- ~w', [Parameters.ip], Command).

hydra_ssh(Parameters, Command) :-
    format_command('hydra -C wordlists/default_credentials/test.txt ~w ssh' , [Parameters.ip], Command).

gobuster_http(Parameters, Command) :-
    format_command('gobuster dir -u http://~w:~w -w wordlists/common.txt', [Parameters.ip, Parameters.port], Command).

gobuster_https(Parameters, Command) :-
    format_command('gobuster dir -u https://~w:~w -w wordlists/common.txt', [Parameters.ip, Parameters.port], Command).

tools(Tool, Command) :-
    profile(Profile, Parameters),
    call(Profile, Parameters, Command),
    tool(Tool, Profile).