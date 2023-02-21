:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).
:- rdf_register_prefix(ns2, 'http://www.semanticweb.org/jef/ontologies/2023/tools#').
:- rdf_load('tools.ttl', [format('turtle')]).

tool(X) :-
    rdfs_individual_of(A, ns2:'Tool'),
    rdf(A,ns2:'name',literal(X)).

profile(X) :-
    rdfs_individual_of(A, ns2:'Profile'),
    rdf(A,ns2:'name',literal(X)).

profile_requirement(Profile,Requirement) :-
    rdfs_individual_of(A, ns2:'Profile'),
    rdf(A,ns2:'hasRequirement',B),
    rdf(A,ns2:'name',literal(Profile)),
    rdf(B,ns2:'requirement',literal(Requirement)).

profile_value(Profile,Value) :-
    rdfs_individual_of(A, ns2:'Profile'),
    rdf(A,ns2:'hasRequirement',B),
    rdf(A,ns2:'name',literal(Profile)),
    rdf(B,ns2:'value',literal(Value)).

profile_result(Profile, Result) :-
    rdfs_individual_of(A, ns2:'Profile'),
    rdf(A,ns2:'hasResult',B),
    rdf(A,ns2:'name',literal(Profile)),
    rdf(B,ns2:'result',literal(Result)).

test_requirements(Requirements, Values) :-
    maplist(call, Requirements, Values).

profile_requirements(Profile, Requirements, Values) :-
    bagof(R, profile_requirement(Profile, R), Requirements),
    %bagof(V, profile_value(Profile, V), Values),
    test_requirements(Requirements, Values) .





