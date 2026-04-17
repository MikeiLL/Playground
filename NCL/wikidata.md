# Wikidata and Spraql

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

They have an API as well: https://www.wikidata.org/wiki/Wikidata:REST_API.
