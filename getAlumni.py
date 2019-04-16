# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """#Katter
SELECT ?uniLabel ?personLabel ?birthLabel ?countryLabel
WHERE 
{
  ?uni wdt:P31 wd:Q3918;
       wdt:P17 wd:Q34.
  ?person wdt:P69 ?uni.
  ?person wdt:P19 ?birth.
  ?birth wdt:P17 ?country.
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

prefix = "@prefix uni:<http://www.semanticweb.org/magnus/ontologies/2019/3/universities#> .\n"
file = open("persons.txt",'a', encoding="utf-8")
file.write(prefix)

for result in results["results"]["bindings"]:
    uni = result['uniLabel']['value']
    name = result['personLabel']['value']
    place = result['birthLabel']['value']
    country = result['countryLabel']['value'] 
    placeFormatted = place.replace(" ","_").replace(".","").replace(",","").replace("(","").replace(")","").replace('\'',"")
    file.write("uni:" + name.replace(" ","_").replace("'","").replace(",","").replace("’","").replace(".","").replace("(","").replace(")",""))
    file.write(" a uni:Person;\n uni:personName \"" + name + "\";\n uni:alumnusOf uni:" + uni.replace(" ","_").replace("'","") + ";\n uni:bornIn uni:" + placeFormatted + ".\n")
    file.write("uni:" + placeFormatted + " a uni:Place; uni:placeName \"" + place + "\"; uni:countryName \"" + country + "\".\n")

file.close()
