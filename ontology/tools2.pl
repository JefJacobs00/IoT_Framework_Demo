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

profileRequirement(Profile,Requirement) :-
    rdfs_individual_of(A, ns2:'Profile'),
    rdf(A,ns2:'hasRequirement',B),
    rdf(A,ns2:'name',literal(Profile)),
    rdf(B,ns2:'requirement',literal(Requirement)).

profileResult(Profile, Result) :-
    rdfs_individual_of(A, ns2:'Profile'),
    rdf(A,ns2:'hasResult',B),
    rdf(A,ns2:'name',literal(Profile)),
    rdf(B,ns2:'result',literal(Result)).


profileRequirements(A, Cs) :-
    bagof(B, profileRequirement(A, B), Cs).





