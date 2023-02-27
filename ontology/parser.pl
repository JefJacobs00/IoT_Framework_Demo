:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/turtle)).
:- use_module(library(semweb/rdfs)).
:- rdf_load(library(semweb/rdfs)).
:- rdf_register_prefix(ns1, 'http://www.semanticweb.org/jef/ontologies/2022/10/demo#').
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




