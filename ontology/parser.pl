:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).
:- rdf_register_prefix(ns1, 'http://www.semanticweb.org/jef/ontologies/2023/demo#').
:- rdf_register_prefix(ns2, 'http://www.semanticweb.org/jef/ontologies/2023/tools#').
:- rdf_load('knowledgebase.ttl', [format('turtle')]).


load_ontology() :-
    rdf_load('knowledgebase.ttl', [format('turtle')]).

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


profileTime(Profile, Time) :-
    rdfs_individual_of(Scan, ns1:'Scan'),
    rdf(Scan, ns1:'epochTime', literal(type('http://www.w3.org/2001/XMLSchema#double',T))),
    atom_number(T, Time),
    rdf(Scan,ns1:'scanInfo',B),
    rdf(B,ns2:'profileName', literal(Profile)).


profileResult(Profile, Result) :-
    rdfs_individual_of(P, ns2:'Profile'),
    rdf(P, ns2:'hasResult', R),
    rdf(R,ns2:'result',literal(Result)),
    rdf(P,ns2:'profileName', literal(Profile)).

profileResults(Profile, Results) :-
    bagof(R, profileResult(Profile,R), Results).

avgProfileDuration(Profile, Avg) :-
    (bagof(Duration, profileDuration(Profile, Duration), List) -> average(List,Avg); Avg = 0).

avgProfileScore(Profile, Avg) :-
    (bagof(Score, profileScore(Profile, Score), List) ->
        (List = [] -> Avg = 0 ; average(List, Avg))
    ; Avg = 0).


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


