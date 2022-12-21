:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).

:- rdf_load('test.ttl', [format('turtle')]).
:- rdf_register_prefix(ns1, 'http://www.semanticweb.org/jef/ontologies/2022/10/demo#').

ip(X) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'ipv4',X).

account(X) :-
    rdfs_individual_of(A, ns1:'Account'),
    rdf(A,ns1:'accountUsername',X).

password(X) :-
    rdfs_individual_of(A, ns1:'Password'),
    rdf(A,ns1:'passwordCleartext',X).

port(X) :-
    rdfs_individual_of(A, ns1:'Password'),
    rdf(A,ns1:'portNumber',X).

devicePorts(Ip, Port) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'addressPort',B),
    rdf(A, ns1:'ipv4', Ip),
    rdf(B, ns1:'portNumber', Port).

deviceSerices(Ip, Service) :-
    rdfs_individual_of(A, ns1:'IpAddress'),
    rdf(A,ns1:'addressPort',B),
    rdf(A, ns1:'ipv4', Ip),
    rdf(B,ns1:'portService',C),
    rdf(C, ns1:'serviceName', Service).




