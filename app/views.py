from django.shortcuts import render
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

# Create your views here.

#imprime na consola os valores cidade - equipa de equipas de inglaterra
def load(request):
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint = endpoint)
    acessor = GraphDBApi(client)
    query = """
            PREFIX fut:<http://worldfootball.org/pred/table/>
            SELECT ?team ?teamname ?pos ?points
            WHERE {
                ?team fut:team ?teamname .
                ?team fut:position ?pos .
                ?team fut:pts ?points .
            }
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body = payload_query, repo_name = repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        print(e['teamname']['value'] + " - " + e['pos']['value'] + " - " + e['points']['value'])
    return render(request, 'index.html', {})