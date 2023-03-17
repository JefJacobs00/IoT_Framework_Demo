:- discontiguous tool/2.
:- discontiguous profile/2.
:- dynamic executed/1.
tool(gobuster, http_dir_scan_small).
tool(gobuster, https_dir_scan_small).
tool(gobuster, http_dir_scan_big).
tool(gobuster, https_dir_scan_big).

profile(http_dir_scan_small, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, http), latestProfileExecution(http_dir_scan_small, Time), get_time(Now), Time + 1000 < Now. 
profile(https_dir_scan_small, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, https), latestProfileExecution(https_dir_scan_small, Time), get_time(Now), Time + 1000 < Now. 
profile(http_dir_scan_big, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, http), latestProfileExecution(http_dir_scan_big, Time), get_time(Now), Time + 1000 < Now. 
profile(https_dir_scan_big, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, https), latestProfileExecution(https_dir_scan_big, Time), get_time(Now), Time + 1000 < Now. 

http_dir_scan_small(Parameters, Command) :- 
	format_command("gobuster dir -u http://~w:~w/ -w wordlists/common.txt", [Parameters.ip, Parameters.port], Command). 

https_dir_scan_small(Parameters, Command) :- 
	format_command("gobuster dir -u https://~w:~w/ -w wordlists/common.txt", [Parameters.ip, Parameters.port], Command). 

http_dir_scan_big(Parameters, Command) :- 
	format_command("gobuster dir -u http://~w:~w/ -w wordlists/big.txt", [Parameters.ip, Parameters.port], Command). 

https_dir_scan_big(Parameters, Command) :- 
	format_command("gobuster dir -u https://~w:~w/ -w wordlists/big.txt", [Parameters.ip, Parameters.port], Command). 

tool(nmap, fast_scan).
tool(nmap, full_scan).

profile(fast_scan, [ip=Ip]) :- ip(Ip), latestProfileExecution(fast_scan, Time), get_time(Now), Time + 1000 < Now. 
profile(full_scan, [ip=Ip]) :- ip(Ip), latestProfileExecution(full_scan, Time), get_time(Now), Time + 1000 < Now. 

fast_scan(Parameters, Command) :- 
	format_command("nmap -F ~w", [Parameters.ip], Command). 

full_scan(Parameters, Command) :- 
	format_command("nmap -sC -sV -p- ~w", [Parameters.ip], Command). 

tool(hydra, ssh_attack).
tool(hydra, ftp_attack).
tool(hydra, telnet_attack).

profile(ssh_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, ssh), latestProfileExecution(ssh_attack, Time), get_time(Now), Time + 1000 < Now. 
profile(ftp_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, ftp), latestProfileExecution(ftp_attack, Time), get_time(Now), Time + 1000 < Now. 
profile(telnet_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, telnet), latestProfileExecution(telnet_attack, Time), get_time(Now), Time + 1000 < Now. 

ssh_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ssh://~w:~w", [Parameters.ip, Parameters.port], Command). 

ftp_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ftp://~w:~w", [Parameters.ip, Parameters.port], Command). 

telnet_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt telnet://~w:~w ", [Parameters.ip, Parameters.port], Command). 

