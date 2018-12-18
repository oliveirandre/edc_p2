from django.shortcuts import render
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from django.template.defaulttags import register
from SPARQLWrapper import  SPARQLWrapper,JSON


# Create your views here.


def tabela(request):
    nomeclube = dict()
    vitorias = dict()
    empates = dict()
    derrotas = dict()
    goaldif = dict()
    posicao = dict()
    pontos = dict()
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint = endpoint)
    acessor = GraphDBApi(client)
    query = """
            PREFIX fut:<http://worldfootball.org/pred/table/>
            SELECT ?team ?teamname ?points ?pos ?hw ?aw ?hd ?ad ?hl ?al ?goaldif
            WHERE {
                ?team fut:team ?teamname .
                ?team fut:position ?pos .
                ?team fut:pts ?points .
                ?team fut:hw ?hw .
                ?team fut:aw ?aw .
                ?team fut:hd ?hd .
                ?team fut:ad ?ad .
                ?team fut:hl ?hl .
                ?team fut:al ?al .
                ?team fut:dif ?goaldif
            }
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body = payload_query, repo_name = repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:

        nomeclube[e['team']['value']] = e['teamname']['value']
        vitorias[e['team']['value']] = int(e['hw']['value']) + int(e['aw']['value'])
        empates[e['team']['value']] = int(e['hd']['value']) + int(e['ad']['value'])
        derrotas[e['team']['value']] = int(e['hl']['value']) + int(e['al']['value'])
        goaldif[e['team']['value']] = e['goaldif']['value']
        posicao[e['team']['value']] = e['pos']['value']
        pontos[e['team']['value']] = e['points']['value']
    tparams = {
        'nomeclube': nomeclube,
        'vitorias': vitorias,
        'empates': empates,
        'derrotas': derrotas,
        'posicaoclube': posicao,
        'golos': goaldif,
        'pontos': pontos,
    }
    print(tparams)
    return render(request, 'tabela.html', tparams)


def jogos(request):
    ronda = dict()
    casa = dict()
    fora = dict()
    resultado = dict()
    estadio = dict()
    quando = dict()
    ganhou = dict()
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    id = dict()
    query = """
            PREFIX fut:<http://worldfootball.org/pred/>
            SELECT ?game ?roundnumber ?home ?away ?result ?stadium ?when
            WHERE {
                ?game <http://worldfootball.org/pred/game/Round_Number> ?roundnumber .
                ?game fut:gameHome_Team ?home .
                ?game fut:gameAway_Team? ?away .
                ?game fut:gameResult ?result .
                ?game fut:gameLocation ?stadium .
                ?game fut:gameDate ?when .
            }
            ORDER BY(?roundnumber)
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        ronda[e['game']['value']] = e['roundnumber']['value']
        casa[e['game']['value']] = e['home']['value']
        fora[e['game']['value']] = e['away']['value']
        resultado[e['game']['value']] = e['result']['value']
        estadio[e['game']['value']] = e['stadium']['value']
        quando[e['game']['value']] = e['when']['value']
        aux = e['result']['value'].split("-")

        aux2 = e['game']['value'].split('/')
        id[e['game']['value']] = aux2[len(aux2)-1]
        if int(aux[0]) > int(aux[1]):
            ganhou[e['game']['value']] = 1
        elif int(aux[0]) < int(aux[1]):
            ganhou[e['game']['value']] = 2
        else:
            ganhou[e['game']['value']] = 0
    
    rounds = dict()

    for e in range(16):
        rounds[e] = str(e+1)

    tparams = {
        'ronda': ronda,
        'casa': casa,
        'fora': fora,
        'resultado': resultado,
        'estadio': estadio,
        'quando': quando,
        'rr': rounds,
        'ganhou': ganhou,
        'id': id
    }
    print(tparams)
    return render(request, 'jogos.html', tparams)


def jogadores(request):
    nome = dict()
    nacionalidade = dict()
    posicao = dict()
    clube = dict()
    idade = dict()
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
            PREFIX player:<http://worldfootball.org/pred/player/>
            SELECT ?id ?name ?club ?age ?position ?nationality
            WHERE {
                ?id player:name ?name .
                ?id player:club ?club .
                ?id player:age ?age .
                ?id player:position ?position .
                ?id player:nationality ?nationality
            }
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        aux=e['name']['value'].split(" ")
        if len(aux)>1:
            nome[e['id']['value']] = aux[1]
        else:
            nome[e['id']['value']] = aux[0]

        nacionalidade[e['id']['value']] = e['nationality']['value']
        posicao[e['id']['value']] = e['position']['value']
        clube[e['id']['value']] = e['club']['value']
        idade[e['id']['value']] = e['age']['value']

    tparams = {
        'nome': nome,
        'nacionalidade': nacionalidade,
        'posicao': posicao,
        'clube': clube,
        'idade': idade
    }
    print(tparams)
    return render(request, 'jogadores.html', tparams)

def main (request):
	return render(request, 'index.html', {})

#def wikidata(request):
#    sparql = SPARQLWrapper("https://query.wikidata.org/")
#    sparql.setQuery("""
#                    SELECT ?itemLabel WHERE {
#                      {
#                      ?item wdt:P31 wd:Q476028.
#                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
#                      }
#                      {
#                      ?item wdt:P118 wd:Q9448
#                      }
#                    }
#                    """)
#    sparql.setReturnFormat(JSON)
#    res = sparql.query().convert()
#    print(res)
#    for res in res['results']['bindings']:
#        print(res['label']['value'])
#    return render(request, 'layout.html', {})

def req (request):
    print(request.POST.get('myInput'))
    return render(request, 'index.html', {})

def jogo (request):
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)

    query = """
                PREFIX fut:<http://worldfootball.org/pred/>
                SELECT ?game ?roundnumber ?home ?away ?result ?stadium ?when
                WHERE {{
                    ?game <http://worldfootball.org/pred/game/Round_Number> ?roundnumber .
                    ?game fut:gameHome_Team ?home .
                    ?game fut:gameAway_Team? ?away .
                    ?game fut:gameResult ?result .
                    ?game fut:gameLocation ?stadium .
                    ?game fut:gameDate ?when .
                    filter( ?game=<http://worldfootball.org/data/game/{0}>)
                }}
                ORDER BY(?roundnumber)
                """.format(str(request.GET['id']))

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        ronda = e['roundnumber']['value']
        casa = e['home']['value']
        fora = e['away']['value']
        resultado = e['result']['value']
        estadio = e['stadium']['value']
        quando = e['when']['value']
        aux = e['result']['value'].split("-")

        if int(aux[0]) > int(aux[1]):
            ganhou = 1
        elif int(aux[0]) < int(aux[1]):
            ganhou = 2
        else:
            ganhou = 0

    rounds = dict()

    for e in range(16):
        rounds[e] = str(e + 1)

    tparams = {
        'ronda': ronda,
        'casa': casa,
        'fora': fora,
        'resultado': resultado,
        'estadio': estadio,
        'quando': quando,
        'rr': rounds,
        'ganhou': ganhou,
    }
    return render(request, 'jogo.html', tparams)


def infoclube(request):
    #pesquisa na base de dados o link para a entidade correspondente na wikidata
    team = "Liverpool"
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
            PREFIX fut:<http://worldfootball.org/pred/table/>
            SELECT ?link ?name
            WHERE {
                ?team fut:team ?name .
                ?team fut:link ?link 
            }
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        if(e['name']['value'] == team):
            wikidata = e['link']['value']
            print(wikidata)

    #em runtime aplica a query sobre a wikidata para obter informação
    sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
    sparql.setQuery("""
                    SELECT DISTINCT  ?item ?itemLabel ?itemDescription
                    WHERE
                      { ?item wdt:P31 wd:Q476028.
                        FILTER ( ?item = <http://www.wikidata.org/entity/Q1130849> )    
                        SERVICE wikibase:label { bd:serviceParam wikibase:language  "en". }
                      }
                    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result)

    return render(request, 'layout.html', {})


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def change(value):
    return value.replace("+"," ")