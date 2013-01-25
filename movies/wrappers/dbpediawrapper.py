# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

from movies.wrappers.base import BaseWrapper


class DBpediaWrapper(BaseWrapper):

    def __init__(self):
        """FIXME: this is just a prototype which won't give you much useful
        data and so has to be rewritten or removed
        """
        self.name = 'dbpedia'
        self.endpoint = SPARQLWrapper('http://dbpedia.org/sparql')
        self.endpoint.setReturnFormat(JSON)

        # query to get movie resources
        # arr this is going to be a complex query...
        self.query_movie = '''
        PREFIX dbpedia2: <http://dbpedia.org/property/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?movie
        WHERE {
            ?movie rdf:type <http://dbpedia.org/ontology/Film>.
            {
                ?movie rdfs:label "%(query_str)s".
            } UNION {
                ?movie rdfs:label "%(query_str)s"@en.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@de.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@es.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@ca.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@cs.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@fi.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@fr.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@it.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@pl.
            } UNION {
                ?movie rdfs:label "%(query_str)s"@uk.
            } UNION {
                ?movie foaf:name "%(query_str)s".
            } UNION {
                ?movie foaf:name "%(query_str)s"@en.
            } UNION {
                ?movie foaf:name "%(query_str)s"@de.
            } UNION {
                ?movie foaf:name "%(query_str)s"@es.
            } UNION {
                ?movie foaf:name "%(query_str)s"@ca.
            } UNION {
                ?movie foaf:name "%(query_str)s"@cs.
            } UNION {
                ?movie foaf:name "%(query_str)s"@fi.
            } UNION {
                ?movie foaf:name "%(query_str)s"@fr.
            } UNION {
                ?movie foaf:name "%(query_str)s"@it.
            } UNION {
                ?movie foaf:name "%(query_str)s"@pl.
            } UNION {
                ?movie foaf:name "%(query_str)s"@uk.
            } UNION {
                ?movie dbpedia2:name "%(query_str)s".
            } UNION {
                ?movie dbpedia2:subTitles "%(query_str)s".
            } UNION {
                ?movie dbpedia2:alttitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:otherTitles "%(query_str)s".
            } UNION {
                ?movie dbpedia2:alternateTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:alternativeTitles "%(query_str)s".
            } UNION {
                ?movie dbpedia2:frenchtitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:suptitles "%(query_str)s".
            } UNION {
                ?movie dbpedia2:internationalTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:altTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:titleOrig "%(query_str)s".
            } UNION {
                ?movie dbpedia2:imdbTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:langTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:englishTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:titled "%(query_str)s".
            } UNION {
                ?movie dbpedia2:workingTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:originalTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:brazilTitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:subtitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:rtitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:englishtitle "%(query_str)s".
            } UNION {
                ?movie dbpedia2:englishtitlea "%(query_str)s".
            } UNION {
                ?movie dbpedia2:englishtitleb "%(query_str)s".
            } UNION {
                ?movie dbpedia2:englishtitlec "%(query_str)s".
            } UNION {
                ?movie dbpedia2:title ?title.
                ?title rdfs:label "%(query_str)s".
            }
        }'''  # for the birds...

    def get_name(self):
        return self.name

    def get_film_by_id(self, film_id):
        movie = self._query_movie_data(film_id)
        return movie

    def get_films_by_name(self, name):
        # get movie resources via SPARQL query
        self.endpoint.setQuery(self.query_movie % {'query_str': name})
        sparql_res = self.endpoint.query().convert()

        movies = []
        for binding in sparql_res['results']['bindings']:
            # FIXME: dummy data
            uri = binding['movie']['value']
            movie = self._query_movie_data(uri)
            movies.append(movie)

        return {'result': movies}

    def _query_movie_data(self, uri):
        """TODO: implement
        """
        pass
