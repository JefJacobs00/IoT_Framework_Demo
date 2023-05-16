:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).
:- rdf_register_prefix(ns1, 'http://www.semanticweb.org/jef/ontologies/2023/demo#').
:- rdf_register_prefix(ns2, 'http://www.semanticweb.org/jef/ontologies/2023/tools#').
:- rdf_load('knowledgebase.ttl', [format('turtle')]).
:- rdf_load('tools.ttl', [format('turtle')]).

load_ontology(Path) :-
    rdf_load(Path, [format('turtle')]).

ipv4(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'IpAddress'),
    rdf(Uri,ns1:'ipv4',literal(X)).

webparam(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'WebParameter'),
    rdf(Uri, ns1:'webParameterName', literal(X)),
    current_session(Uri).


page(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'Webpage'),
    rdf(Uri, ns1:'page', literal(X)),
    current_session(Uri).

webpage_param(Page, Parameter) :-
    rdfs_individual_of(A, ns1:'Webpage'),
    rdf(B,ns1:'webpageParameter',A),
    rdf(A,ns1:'page',literal(Page)),
    rdf(B,ns1:'webParameterName',literal(Parameter)),
    page(Page , _),
    webparam(Parameter, _).


account(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'Account'),
    rdf(Uri,ns1:'accountUsername',literal(X)),
    current_session(Uri).

password(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'Password'),
    rdf(Uri,ns1:'passwordCleartext',literal(X)),
    current_session(Uri).

accountPassword(Account, Password) :-
    rdfs_individual_of(A, ns1:'Account'),
    rdf(A,ns1:'accountPassword',B),
    rdf(A,ns1:'accountUsername',literal(Account)),
    rdf(B,ns1:'passwordCleartext',literal(Password)),
    account(Account , _),
    password(Password, _).


port(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'Port'),
    rdf(Uri,ns1:'portNumber',literal(X)),
    current_session(Uri).

hashValue(Hash, Uri) :-
    rdfs_individual_of(Uri, ns1:'Hash'),
    rdf(Uri, ns1:'hashValue',literal(Hash)),
    current_session(Uri).

passwordHash(Hash, Password) :-
    rdfs_individual_of(A, ns1:'Hash'),
    rdf(B,ns1:'passwordHash',A),
    rdf(A,ns1:'hashValue',literal(Hash)),
    rdf(B,ns1:'passwordCleartext',literal(Password)),
    hashValue(Hash, _).

firmware(Path, Uri) :-
    rdfs_individual_of(Uri, ns1:'Firmware'),
    rdf(Uri,ns1:'firmwarePath',literal(Path)).

service(X, Uri) :-
    rdfs_individual_of(Uri, ns1:'Service'),
    rdf(Uri,ns1:'serviceName',literal(X)),
    current_session(Uri).

devicePorts(Ip, Port) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'addressPort',B),
    rdf(A, ns1:'ipv4', literal(Ip)),
    rdf(B, ns1:'portNumber', literal(Port)).

deviceServices(Ip, Port, Service) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'addressPort',B),
    rdf(B, ns1:'portNumber', literal(Port)),
    rdf(A, ns1:'ipv4', literal(Ip)),
    rdf(B,ns1:'portService',C),
    rdf(C, ns1:'serviceName', literal(Service)).


profileDuration(Profile, Duration) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'duration', literal(type('http://www.w3.org/2001/XMLSchema#double', D))),
    atom_number(D, Duration),
    rdf(Scan,ns1:'scanInfo',B),
    rdf(B,ns2:'profileName',literal(Profile)).


profileScore(Profile, Score) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'resultScore', literal(type('http://www.w3.org/2001/XMLSchema#double',S))),
    atom_number(S, Score),
    rdf(Scan,ns1:'scanInfo',B),
    rdf(B,ns2:'profileName', literal(Profile)).

profileScans(Profile, Scan) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'scanProfile',P),
    rdf(P, ns2:'profileName', literal(Profile)).

scans(Scan) :-
    rdfs_individual_of(Scan, ns1:'Scan').

scanCommand(Scan, Command) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'command', literal(Command)).


scanInfo(Scan, Info) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Info, ns1:'scanInfo', Scan).

profile(Profile) :-
    rdfs_individual_of(P, ns2:'Profile'),
    rdf(P, ns2:'profileName', literal(Profile)).

profileTime(Profile, Time) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'epochTime', literal(type('http://www.w3.org/2001/XMLSchema#double',T))),
    atom_number(T, Time),
    rdf(Scan,ns1:'scanProfile',B),
    rdf(B,ns2:'profileName', literal(Profile)).

scanTime(Scan, Time) :-
rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'epochTime', literal(type('http://www.w3.org/2001/XMLSchema#double',T))),
    atom_number(T, Time).


profileResult(Profile, Result) :-
    rdfs_individual_of(P, ns2:'Profile'),
    rdf(P, ns2:'hasResult', R),
    rdf(R,ns2:'result',literal(Result)),
    rdf(P,ns2:'profileName', literal(Profile)).


checkAttackChain(Parameter) :-
    get_last_scan(X),
    setof(P, scanInfo(X, P), Parameters),
    member(Parameter, Parameters).

checkChainProfile([]).
checkChainProfile([H | T]) :-
    checkChainProfile(T),
    checkAttackChain(H).

% Vergelijken parameters met results
% Wanneer een result gebruikt wordt als parameter + punten

profileParameter(Profile, Parameter) :- 
    rdfs_individual_of(P, ns2:'Profile'),
    rdf(P, ns2:'hasParameter', Par),
    rdf(Par, ns2:'parameter', literal(Parameter)),
    rdf(P, ns2:'profileName', literal(Profile)).

scanInput(Scan, Input) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'scanInput', Info),
    rdf(Info, ns1:'ParameterURI', literal(Input)).


profileDemand(Profile, Count) :-
    bagof(Result, profileResult(Profile, Result), Results),
    demandResults(Results, Count).


demandResults([], 0).
demandResults([H | T], Count) :-
    demandResults(T, C1),
    checkParameterCount(H, C2),
    Count is C1 + C2.

checkParameterCount(Result, Count) :-
    bagof(Profile, profile(Profile), Profiles),
    parameterCounter(Profiles, Result, Count).

parameterCounter([], _, 0).
parameterCounter([H | T], Parameter, N) :-
    parameterCounter(T, Parameter, N1),
    (profileParameter(H, Parameter) -> N = 1 + N1; N is N1).


checkUsefullnessProfile(Profile, InfoUsed) :-
    bagof(S,profileScans(Profile, S),Scans),
    checkUsefullnessScans(Scans, InfoUsed).

checkUsefullnessScans([], 0).
checkUsefullnessScans([Scan | Scans], InfoUses) :-
    checkUsefullnessScans(Scans, C1),
    (bagof(I, scanInfo(Scan, I), Info) ->
        checkInputUses(Info, C2), InfoUses is C1 + C2;
        InfoUses is C1
    ).


checkInputUses([], 0).
checkInputUses([Info | T], Count) :-
    checkInputUses(T, C1),
    checkInfoUse(Info, C2),
    Count is C1 + C2.

checkInfoUse(Input, Count) :-
    (bagof(Scan, scanInput(Scan, Input), Scans) -> length(Scans, Count); Count is 0).

avgProfileDuration(Profile, Avg) :-
    (bagof(Duration, profileDuration(Profile, Duration), List) -> average(List,Avg); Avg = 0).

totalProfileInfo(Profile, N) :-
    bagof(Scan, profileScans(Profile, Scan), Scans),
    count_profile_info(Scans, N).

profileConsistencyRate(Profile, Rate) :-
    (maxProfileInfo(Profile, M) -> Max is M; Max is 1),
    (averageProfileInfo(Profile, A) -> Avg is A; Avg is 1),
    Rate is Avg/Max.

maxProfileInfo(Profile, Max) :-
    listProfileInfo(Profile, List),
    max_member(M, List),
    (M == 0 -> Max is 0.000000001; Max is M).

averageProfileInfo(Profile, Average) :-
    listProfileInfo(Profile, List),
    sumlist(List, Sum),
    count(List, Count),
    Average is Sum/Count.

listProfileInfo(Profile, List) :-
    bagof(Scan, profileScans(Profile, Scan), Scans),
    getAmountScanInfo(Scans, List).

current_session(Parameter) :-
    get_last_parameter_scan(Parameter, Scan),
    is_last_scan(Scan),
    scanCommand(Scan, Command),
    atom_codes(Command, Codes),
    string_codes(String_Command, Codes),
    executed(_, String_Command).

is_last_scan(Scan) :-
    scanCommand(Scan, Command),
    bagof(S, scanCommand(S,Command), Scans),
    last(Scans, _, LastScan),!,
    LastScan == Scan.

get_last_scan(LastScan) :-
    findall(S, scanInfo(S, _), Scans),
    last(Scans,_, LastScan), !.

get_last_parameter_scan(Parameter, LastScan) :-
    bagof(S, scanInfo(S, Parameter), Scans),
    last(Scans, _, LastScan), !.

last([],-1, _).
last([H | T], Max, LastScan) :-
    last(T, Max1, Scan),
    scan_number(H, N2),
    (Max1 > N2 -> (LastScan = Scan, Max = Max1); (LastScan = H, Max = N2)).


scan_number(Scan, Number) :-
    string_to_list(Scan, ScanList),
    reverse(ScanList, Reversed),
    get_number(Reversed, X), reverse(X, NumberList), atom_chars(NumberStr, NumberList), atom_number(NumberStr, Number).

get_number([], []).
get_number([H | _], []) :- H < 47 ; H > 58.
get_number([H | T], [H | R]) :-
    H >= 47,
    H =< 58,
    get_number(T, R).
get_number([_ | T], R) :-
    get_number(T, R).


getAmountScanInfo([],[]).
getAmountScanInfo([H | T], List) :-
    getAmountScanInfo(T, L),
    amountOfScanInfo(H, N),
    append(L, [N], List).

amountOfScanInfo(Scan, N) :-
    (bagof(I, scanInfo(Scan, I), In) -> Info = In; Info = []),
    count(Info, N).

count_profile_info([], 0).
count_profile_info([H | T], N) :-
    count_profile_info(T , N1),
    amountOfScanInfo(H, N2),
    N is N1 + N2.

count([], 0).
count([_|T], N) :-
    count(T, N1),
    N is N1+1.

latestProfileExecution(Profile, Max) :-
    (bagof(Time, profileTime(Profile, Time), Times) -> max_value(Times, Max); Max = 0).

max_value([H], H).
max_value([H|T], Max) :-
    max_value(T, Max1),
    (H > Max1 -> Max = H ; Max = Max1).

average(List, Average) :-
    sumlist( List, Sum ),
    length( List, Length ),
    (Length > 0) -> Average is Sum / Length; Average = 0.


