# Wikidata and Spraql

Wikidata query tool can be used to aggregate data. For example I wanted to pull up a bunch of items related to Pokémon.

This query brings up over 1,000 Pokémon items. Run it [here](https://query.wikidata.org/).
```sparql
SELECT DISTINCT ?item ?itemLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P1685 ?statement0.
      ?statement0 (ps:P1685) _:anyValueP1685.
    }
    LIMIT 5000
  }
}
```

On the [main page](https://www.wikidata.org/wiki/Wikidata:Main_Page) you can search by Property (among other types). This is how I identified the [Pokémon index](https://www.wikidata.org/wiki/Property:P1685) which has the id of `P1685` used in the above query. As a beginner to SPARQL I used the [query builder](https://query.wikidata.org/querybuilder) to build the query, then the link to [show the query in the query service](https://query.wikidata.org/#SELECT%20DISTINCT%20?item%20?itemLabel%20WHERE%20%7B%0A%20%20SERVICE%20wikibase:label%20%7B%20bd:serviceParam%20wikibase:language%20%22%5BAUTO_LANGUAGE%5D,mul,en%22.%20%7D%0A%20%20%7B%0A%20%20%20%20SELECT%20DISTINCT%20?item%20WHERE%20%7B%0A%20%20%20%20%20%20?item%20p:P1685%20?statement0.%0A%20%20%20%20%20%20?statement0%20(ps:P1685)%20_:anyValueP1685.%0A%20%20%20%20%7D%0A%20%20%20%20LIMIT%201500%0A%20%20%7D%0A%7D) to get the above SPARQL.

This [intro to SPARQL](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial) query language is worth reading.

They have an API as well: https://www.wikidata.org/wiki/Wikidata:REST_API.
