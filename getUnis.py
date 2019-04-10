# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """#Katter
SELECT ?uniLabel #?personLabel ?empLabel
WHERE 
{
  ?uni wdt:P31 wd:Q3918;
       wdt:P17 wd:Q34.
  #?person wdt:P69 ?uni.
  #?person wdt:P108 ?emp.
  #?emp wdt:P31 wd:Q43229.
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}"""


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)
