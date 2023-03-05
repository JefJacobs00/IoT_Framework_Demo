tool(gobuster, http_dir_scan_small).
tool(gobuster, https_dir_scan_small).
tool(gobuster, http_dir_scan_big).
tool(gobuster, https_dir_scan_big).

profile(http_dir_scan_small, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, http). 
profile(https_dir_scan_small, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, https). 
profile(http_dir_scan_big, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, http). 
profile(https_dir_scan_big, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, https). 

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

profile(fast_scan, [ip=Ip]) :- ip(Ip). 
profile(full_scan, [ip=Ip]) :- ip(Ip). 

fast_scan(Parameters, Command) :- 
	format_command("nmap -F ~w", [Parameters.ip], Command). 

full_scan(Parameters, Command) :- 
	format_command("nmap -sC -sV -p- ~w", [Parameters.ip], Command). 

tool(hydra, ssh_attack).
tool(hydra, ftp_attack).
tool(hydra, telnet_attack).

profile(ssh_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, ssh). 
profile(ftp_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, ftp). 
profile(telnet_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, telnet). 

ssh_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ssh://~w:~w", [Parameters.ip, Parameters.port], Command). 

ftp_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ftp://~w:~w", [Parameters.ip, Parameters.port], Command). 

telnet_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt telnet://~w:~w ", [Parameters.ip, Parameters.port], Command). 

