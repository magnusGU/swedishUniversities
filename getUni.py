# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
# 
#
# example:
# @prefix uni:<http://www.semanticweb.org/magnus/ontologies/2019/3/universities#> .
#
# uni:kth a uni:University;
#         uni:organisationName "kth".

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """
SELECT ?uniLabel ?year ?placeLabel ?countryLabel
WHERE 
{
  ?uni wdt:P31 wd:Q3918;
       wdt:P17 wd:Q34.
  ?uni wdt:P571 ?year.
  ?uni wdt:P131 ?place.
  ?uni wdt:P17 ?country.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_DETECT],en". }
}"""



def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

prefix = "@prefix uni:<http://www.semanticweb.org/magnus/ontologies/2019/3/universities#> ."
file = open("universityNames.txt",'a', encoding="utf-8")
file.write(prefix)
for result in results["results"]["bindings"]:
    year = result['year']['value'][0:4]
    name = result['uniLabel']['value']
    place = result['placeLabel']['value']
    country = result['countryLabel']['value']
    if place.endswith(" Municipality"):
        place = place.replace(" Municipality","")

    file.write("\nuni:" + name.replace(" ","_").replace("'","") + " a uni:University;\n" + " uni:organisationName \"" + name +"\";\n uni:yearFounded \"" + year + "\"; uni:locatedIn uni:" + place.replace(" ","")+ ". \n")
    file.write("uni:" + place.replace(" ","") + " a uni:Place; uni:placeName \"" + place + "\"; uni:countryName \"" + country + "\".")
    
file.close()    
