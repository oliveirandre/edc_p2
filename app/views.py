from django.shortcuts import render
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

# Create your views here.

#imprime na consola os valores cidade - equipa de equipas de inglaterra
def load(request):
    endpoint = "http://localhost:7200"
    repo_name = "stadiums"
    client = ApiClient(endpoint = endpoint)
    acessor = GraphDBApi(client)
    query = """
            PREFIX stad:<http://stadiums.org/pred/>
            SELECT ?city ?teamname
            WHERE {
                ?city stad:country "England" .
                ?city stad:team ?teamname .
            }
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body = payload_query, repo_name = repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        a, b, c, d = e['city']['value'].split("/")
        print(d + ' - ' + e['teamname']['value'])
    return render(request, 'index.html', {})