:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).

:- rdf_load('test.ttl', [format('turtle')]).
:- rdf_register_prefix(ns1, 'http://www.semanticweb.org/jef/ontologies/2022/10/demo#').

ip(X) :-
    rdfs_individual_of(X, ns1:'IpAddress').

:- rdf_meta
    ip(r).

account(X) :-
    rdfs_individual_of(X, ns1:'Account').

:- rdf_meta
    account(r).

password(X) :-
    rdfs_individual_of(X, ns1:'Password').

:- rdf_meta
    password(r).


