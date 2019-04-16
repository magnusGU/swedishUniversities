from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?uniLabel ?yearLabel ?placeLabel ?unicountryLabel ?personLabel ?birthLabel ?countryLabel ?empLabel ?empPlaceLabel ?empCountryLabel
WHERE 
{
  ?uni wdt:P31 wd:Q3918;
       wdt:P17 wd:Q34.
  ?uni wdt:P571 ?year.
  ?uni wdt:P131 ?place.
  ?uni wdt:P17 ?unicountry.
  
  ?person wdt:P69 ?uni.
  ?person wdt:P19 ?birth.
  ?birth wdt:P17 ?country.
  ?person wdt:P108 ?emp.
  ?emp wdt:P131 ?empPlace.
  ?empPlace wdt:P17 ?empCountry.
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}"""


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

prefix = "@prefix uni:<http://www.semanticweb.org/magnus/ontologies/2019/3/universities#> .\n"
file = open("allinfo.txt",'a', encoding="utf-8")
file.write(prefix)

for result in results["results"]["bindings"]:
    year = result['yearLabel']['value'][0:4]
    uniname = result['uniLabel']['value']
    place = result['placeLabel']['value']
    unicountry = result['unicountryLabel']['value']
    if place.endswith(" Municipality"):
        place = place.replace(" Municipality","")

    file.write("\nuni:" + uniname.replace(" ","_").replace("'","") + " a uni:University;\n" + " uni:organisationName \"" + uniname +"\";\n uni:yearFounded \"" + year + "\"; uni:locatedIn uni:" + place.replace(" ","")+ ". \n")
    file.write("uni:" + place.replace(" ","") + " a uni:Place; uni:placeName \"" + place + "\"; uni:countryName \"" + unicountry + "\".\n")

    name = result['personLabel']['value']
    birthplace = result['birthLabel']['value']
    country = result['countryLabel']['value'] 
    placeFormatted = birthplace.replace(" ","_").replace(".","").replace(",","").replace("(","").replace(")","").replace('\'',"").replace("–","-")
    file.write("uni:" + name.replace(" ","_").replace("'","").replace(",","").replace("’","").replace(".","").replace("(","").replace(")",""))
    file.write(" a uni:Person;\n uni:personName \"" + name + "\";\n uni:alumnusOf uni:" + uniname.replace(" ","_").replace("'","") + ";\n uni:bornIn uni:" + placeFormatted + ".\n")
    file.write("uni:" + placeFormatted + " a uni:Place; uni:placeName \"" + birthplace + "\"; uni:countryName \"" + country + "\".\n")

    emp = result['empLabel']['value']
    empPlace = result['empPlaceLabel']['value']
    empCountry = result['empCountryLabel']['value']
    empFormatted = emp.replace(" ","_").replace(".","").replace(",","").replace("(","").replace(")","").replace('\'',"").replace("–","-")
    empPlaceFormatted = empPlace.replace(" ","_").replace(".","").replace(",","").replace("(","").replace(")","").replace('\'',"").replace("–","-")
    file.write('uni:'+empFormatted+ " a uni:Organisation; uni:organisationName \"" + emp + "\"; uni:locatedIn uni:"+empPlaceFormatted+". \n")
    file.write("uni:"+empPlaceFormatted + " a uni:Place; uni:placeName \""+empPlace+"\"; uni:countryName \"" +empCountry+"\" . \n" )

file.close()