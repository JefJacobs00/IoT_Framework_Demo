:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).
:- rdf_register_prefix(ns1, 'http://www.semanticweb.org/jef/ontologies/2023/demo#').
:- rdf_register_prefix(ns2, 'http://www.semanticweb.org/jef/ontologies/2023/tools#').
:- rdf_load('knowledgebase.ttl', [format('turtle')]).


load_ontology() :-
    rdf_load('ontology/knowledgebase.ttl', [format('turtle')]).

ip(X) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'ipv4',literal(X)).

account(X) :-
    rdfs_individual_of(A, ns1:'Account'),
    rdf(A,ns1:'accountUsername',literal(X)).

password(X) :-
    rdfs_individual_of(A, ns1:'Password'),
    rdf(A,ns1:'passwordCleartext',literal(X)).

port(X) :-
    rdfs_individual_of(A, ns1:'Port'),
    rdf(A,ns1:'portNumber',literal(X)).

service(X) :-
    rdfs_individual_of(A, ns1:'Service'),
    rdf(A,ns1:'serviceName',literal(X)).

devicePorts(Ip, Port) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'addressPort',B),
    rdf(A, ns1:'ipv4', literal(Ip)),
    rdf(B, ns1:'portNumber', literal(Port)).

passwordHash(Hash) :-
    rdfs_individual_of(A, ns1:'Hash'),
    rdf(A, ns1:'hashValue',literal(Hash)).

firmware(Path) :-
    rdfs_individual_of(A, ns1:'Firmware'),
    rdf(A,ns1:'firmwarePath',Path).

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

scanInfo(Scan, Info) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Info, ns1:'scanInfo', Scan).


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

avgProfileDuration(Profile, Avg) :-
    (bagof(Duration, profileDuration(Profile, Duration), List) -> average(List,Avg); Avg = 0).

totalProfileInfo(Profile, N) :-
    bagof(Scan, profileScans(Profile, Scan), Scans),
    count_profile_info(Scans, N).

listProfileInfo(Profile, List) :-
    bagof(Scan, profileScans(Profile, Scan), Scans),
    getAmountScanInfo(Scans, List).

get_last_scan(Scan) :-
    bagof(S, scans(S), Scans),
    highest_value_uri(Scans, Scan).

get_uri_value(Uri, Value) :-
    write(Uri),
    atom_codes(Uri, Codes),
    reverse(Codes, RevCodes),
    take_while(is_digit, RevCodes, DigitCodes),
    reverse(DigitCodes, RevDigitCodes),
    number_codes(V, RevDigitCodes),
    (scanInfo(Uri, _) -> Value = V; Value = 0).

take_while(_, [], []).
take_while(Pred, [X|Xs], [X|Ys]) :-
    call(Pred, X),
    take_while(Pred, Xs, Ys).
take_while(_, _, []).

highest_value_uri(UriList, HighestUri) :-
    maplist(get_uri_value, UriList, ValueList),
    max_list(ValueList, MaxValue),
    nth0(Index, ValueList, MaxValue),
    nth0(Index, UriList, HighestUri).


check_value([H], H, Value) :-
    get_uri_value(H, Value).
check_value([H | T], HighestUri, Value) :-
    check_value(T, HighestUri, V0),
    get_uri_value(H, V1),
    (V1 > V0 -> Value = V1; Value = V0).

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


