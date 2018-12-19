from django.shortcuts import render
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from django.template.defaulttags import register
from SPARQLWrapper import  SPARQLWrapper,JSON
from django.http import HttpResponseRedirect

# Create your views here.


def tabela(request):
    nomeclube = dict()
    vitorias = dict()
    empates = dict()
    derrotas = dict()
    goaldif = dict()
    posicao = dict()
    pontos = dict()
    link = dict()
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint = endpoint)
    acessor = GraphDBApi(client)
    query = """
            PREFIX fut:<http://worldfootball.org/pred/table/>
            SELECT ?team ?teamname ?points ?pos ?hw  ?hd  ?hl  ?goaldif ?link
            WHERE {
                ?team fut:team ?teamname .
                ?team fut:position ?pos .
                ?team fut:pts ?points .
                ?team fut:hw ?hw .
                ?team fut:hd ?hd .
                ?team fut:hl ?hl .
                ?team fut:dif ?goaldif.
                ?team fut:link ?link
            }
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body = payload_query, repo_name = repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:

        nomeclube[e['team']['value']] = e['teamname']['value']
        vitorias[e['team']['value']] = int(e['hw']['value'])
        empates[e['team']['value']] = int(e['hd']['value'])
        derrotas[e['team']['value']] = int(e['hl']['value'])
        goaldif[e['team']['value']] = e['goaldif']['value']
        posicao[e['team']['value']] = e['pos']['value']
        pontos[e['team']['value']] = e['points']['value']
        aux=e['team']['value'].split('/')
        aux2=e['link']['value'].split('/')
        link[e['team']['value']] = aux2[len(aux2)-1]

    tparams = {
        'nomeclube': nomeclube,
        'vitorias': vitorias,
        'empates': empates,
        'derrotas': derrotas,
        'posicaoclube': posicao,
        'golos': goaldif,
        'pontos': pontos,
        'link' : link
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
    id=dict()
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
        aux=e['id']['value'].split('/')
        id[e['id']['value']]=aux[len(aux)-1]


    tparams = {
        'nome': nome,
        'nacionalidade': nacionalidade,
        'posicao': posicao,
        'clube': clube,
        'idade': idade,
        'id' : id
    }
    print(tparams)
    return render(request, 'jogadores.html', tparams)

def main (request):
	return render(request, 'index.html', {})


def req (request):
    print(request.POST.get('myInput'))

    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
                PREFIX fut:<http://worldfootball.org/pred/table/>
                SELECT ?team ?teamname ?points ?pos ?hw ?aw ?hd ?ad ?hl ?al ?goaldif ?link
                WHERE {{
                    ?team fut:team ?teamname .
                    ?team fut:position ?pos .
                    ?team fut:pts ?points .
                    ?team fut:hw ?hw .
                    ?team fut:aw ?aw .
                    ?team fut:hd ?hd .
                    ?team fut:ad ?ad .
                    ?team fut:hl ?hl .
                    ?team fut:al ?al .
                    ?team fut:dif ?goaldif.
                    ?team fut:link ?link.
                    FILTER (?teamname = "{0}")
                }} 
                """.format(request.POST.get('myInput'))

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        aux2 = e['link']['value'].split('/')
        link = aux2[len(aux2) - 1]

    return HttpResponseRedirect('equipa?entity='+link)

def jogo (request):

    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)

    #info game
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

    query = """
            PREFIX fut:<http://worldfootball.org/pred/table/>
            SELECT ?team ?teamname ?link 
            WHERE {{
                ?team fut:team ?teamname.
                ?team fut:link ?link.
                FILTER (?teamname = "{0}")
            }}
            """.format(casa)



    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        aux = e['link']['value'].split('/')
        casalink=aux[len(aux)-1]

    query = """
              PREFIX fut:<http://worldfootball.org/pred/table/>
              SELECT ?team ?teamname ?link
              WHERE {{
                  ?team fut:team ?teamname.
                  ?team fut:link ?link.
                  FILTER (?teamname = "{0}")
                  
              }}
              """.format(fora)

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        aux = e['link']['value'].split('/')
        foralink = aux[len(aux) - 1]



    #estadio
    query = """
                   PREFIX stad:<http://worldfootball.org/pred/stadium/>
                   SELECT ?team ?link
                   WHERE {{
                       ?stadium stad:link ?link .
                       ?stadium stad:FDCOUK ?team .
                       FILTER (?team = "{0}")
                   }}
                   """.format(casa)

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:
        estadiolink = e['link']['value']

        # estadio
    sparql2 = SPARQLWrapper("http://query.wikidata.org/sparql")
    query2 = """
               SELECT ?itemLabel ?image
               WHERE 
               {{
                 ?item wdt:P31 wd:Q483110.
                 ?item wdt:P18 ?image.
                 FILTER (?item = <{0}> )
                 SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
               }}
               """.format(estadiolink)

    sparql2.setQuery(query2)
    sparql2.setReturnFormat(JSON)
    results = sparql2.query().convert()
    image = ""
    for result in results['results']['bindings']:
        image = result['image']['value']

    # estadio
    query2 = """
                  SELECT ?itemLabel ?image
                  WHERE 
                  {{
                    ?item wdt:P31 wd:Q1154710.
                    ?item wdt:P18 ?image.
                    FILTER (?item = <{0}> )
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
                  }}
                  """.format(estadiolink)
    sparql2.setQuery(query2)
    sparql2.setReturnFormat(JSON)
    results = sparql2.query().convert()
    for result in results['results']['bindings']:
        image = result['image']['value']

    sparql2.setQuery(query2)
    sparql2.setReturnFormat(JSON)
    results = sparql2.query().convert()

    for result in results['results']['bindings']:
        image = result['image']['value']


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
        'casalink': casalink,
        'foralink':foralink,
        'image' : image
    }
    return render(request, 'jogo.html', tparams)


def infoclube(request):

    link = 'http://www.wikidata.org/entity/' + request.GET['entity']
    #em runtime aplica a query sobre a wikidata para obter informação
    sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
    query2 = """
             SELECT ?itemLabel ?date ?locationLabel ?coachLabel ?stadiumLabel ?stadium ?site
             WHERE
              {{ 
                 ?item wdt:P571 ?date.
                 ?item wdt:P159 ?location.
                 ?item wdt:P286 ?coach.
                 ?item wdt:P115 ?stadium.
                 ?item wdt:P856 ?site.
                FILTER ( ?item = <{0}> ) 
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
              }}
              """.format(link)
    sparql.setQuery(query2)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results['results']['bindings']:
        stad = result['stadium']['value']
        nome = result['itemLabel']['value']
        aux = result['date']['value'].split('T')
        data = aux[0]
        site = result['site']['value']

        cidade = result['locationLabel']['value']
        treinador = result['coachLabel']['value']
        estadio = result['stadiumLabel']['value']

    #tabela
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
                        PREFIX fut:<http://worldfootball.org/pred/table/>
                        SELECT  ?points ?pos ?hw  ?hd  ?hl  ?goaldif ?link
                        WHERE {{
                            ?team fut:hw ?hw .
                            ?team fut:position ?pos .
                            ?team fut:hd ?hd .
                            ?team fut:hl ?hl .
                            ?team fut:pts ?points .
                            ?team fut:dif ?goaldif.
                            ?team fut:link ?link.
                            FILTER (?link = <{0}>)
                        }} 
                        """.format(link)

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:
        vitorias = int(e['hw']['value'])
        empates = int(e['hd']['value'])
        derrotas = int(e['hl']['value'])
        goaldif = e['goaldif']['value']
        posicao = e['pos']['value']
        pontos = e['points']['value']

    #estadio
    sparql2 = SPARQLWrapper("http://query.wikidata.org/sparql")
    query2 = """
            SELECT ?itemLabel ?image
            WHERE 
            {{
              ?item wdt:P31 wd:Q483110.
              ?item wdt:P18 ?image.
              FILTER (?item = <{0}> )
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
            }}
            """.format(stad)

    sparql2.setQuery(query2)
    sparql2.setReturnFormat(JSON)
    results = sparql2.query().convert()
    image=""
    for result in results['results']['bindings']:
        image = result['image']['value']

    #estadio
    query2 = """
               SELECT ?itemLabel ?image
               WHERE 
               {{
                 ?item wdt:P31 wd:Q1154710.
                 ?item wdt:P18 ?image.
                 FILTER (?item = <{0}> )
                 SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
               }}
               """.format(stad)
    sparql2.setQuery(query2)
    sparql2.setReturnFormat(JSON)
    results = sparql2.query().convert()
    for result in results['results']['bindings']:
        image = result['image']['value']


    query = """
                PREFIX stad:<http://worldfootball.org/pred/stadium/>
                SELECT ?capacity ?team
                WHERE {{
                    ?stadium stad:link ?link .
                    ?stadium stad:teamlink ?team .
                    ?stadium stad:Capacity ?capacity
                    FILTER (?link = <{0}>)
                }}
                """.format(stad)
    print(query)
    capacidade=""
    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        capacidade = e['capacity']['value']


    tparams = {
        'nome': nome,
        'data': data,
        'cidade': cidade,
        'treinador': treinador,
        'estadio': estadio,
        'vitorias': vitorias,
        'empates': empates,
        'derrotas': derrotas,
        'posicaoclube': posicao,
        'golos': goaldif,
        'pontos': pontos,
        'imageS' : image,
        'capacidade' : capacidade,
        'site' : site
    }




    return render(request, 'clube.html', tparams)

def edit_club(request):

    link = 'http://www.wikidata.org/entity/' + request.GET['entity']
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
                            PREFIX fut:<http://worldfootball.org/pred/table/>
                            SELECT ?team ?teamname ?points ?pos ?hw ?hd  ?hl ?goaldif ?link
                            WHERE {{
                                ?team fut:team ?teamname .
                                ?team fut:hw ?hw .
                                ?team fut:position ?pos .
                                ?team fut:hd ?hd .
                                ?team fut:hl ?hl .
                                ?team fut:pts ?points .
                                ?team fut:dif ?goaldif.
                                ?team fut:link ?link.
                                FILTER (?link = <{0}>)
                            }} 
                            """.format(link)

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:
        vitorias = int(e['hw']['value'])
        empates = int(e['hd']['value'])
        derrotas = int(e['hl']['value'])
        goaldif = e['goaldif']['value']
        posicao = e['pos']['value']
        pontos = e['points']['value']
        nome = e['teamname']['value']
        aux = e['team']['value'].split('/')
        id = aux[len(aux)-1]

    tparams={
        'vitorias': vitorias,
        'empates': empates,
        'derrotas': derrotas,
        'posicaoclube': posicao,
        'golos': goaldif,
        'pontos': pontos,
        'nome': nome,
        'id' : id
    }
    return render(request, 'editar_clube.html', tparams)

def edit(request):
    pontos = request.POST.get('pontos')
    posicaoclube = request.POST.get('posicaoclube')
    vitorias = request.POST.get('vitorias')
    empates = request.POST.get('empates')
    derrotas = request.POST.get('derrotas')
    golos = request.POST.get('golos')
    nome = request.POST.get('Nome')
    id = "<http://worldfootball.org/suj/table/" + request.POST.get('id') + ">"

    pontos_ = request.POST.get('pontos_')
    posicaoclube_ = request.POST.get('posicaoclube_')
    vitorias_ = request.POST.get('vitorias_')
    empates_ = request.POST.get('empates_')
    derrotas_ = request.POST.get('derrotas_')
    golos_ = request.POST.get('golos_')


    if(int(golos) > 0):
        if "+" not in golos:
            golos = "+" + str(golos)

    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
                PREFIX table:<http://worldfootball.org/pred/table/>
                DELETE DATA {{
                    {0} table:pts "{1}" .
                    {0} table:dif "{2}" .
                    {0} table:position "{3}" .
                    {0} table:hw "{4}" .
                    {0} table:hd "{5}" .
                    {0} table:hl "{6}" .
                }}
            """.format(id, pontos_, golos_, posicaoclube_, vitorias_, empates_, derrotas_ )
    print(query)
    payload_query = {"update": query}
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name)

    query2 = """
                PREFIX table:<http://worldfootball.org/pred/table/>
                INSERT DATA {{
                    {0} table:pts "{1}" .
                    {0} table:dif "{2}" .
                    {0} table:position "{3}" .
                    {0} table:hw "{4}" .
                    {0} table:hd "{5}" .
                    {0} table:hl "{6}" .
                 }}
                """.format(id, pontos, golos, posicaoclube, vitorias, empates, derrotas)
    payload_query = {"update": query2}
    res2 = acessor.sparql_update(body=payload_query, repo_name=repo_name)

    return render(request, 'layout.html',{})

def jogador (request):
    endpoint = "http://localhost:7200"
    repo_name = "football"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)

    query =  """
                PREFIX player:<http://worldfootball.org/pred/player/>
                SELECT ?id ?name ?club ?age ?position ?nationality
                WHERE {{
                    ?id player:name ?name .
                    ?id player:club ?club .
                    ?id player:age ?age .
                    ?id player:position ?position .
                    ?id player:nationality ?nationality
                    filter( ?id=<http://worldfootball.org/data/player/{0}>)
            }}
            """.format(str(request.GET['id']))

    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    print(res)
    for e in res['results']['bindings']:
        nome = e['name']['value']
        nacionalidade = e['nationality']['value']
        posicao = e['position']['value']
        clube = e['club']['value']
        idade = e['age']['value']

    tparams = {
        'nacionalidade': nacionalidade,
        'nome': nome,
        'posicao': posicao,
        'clube': clube,
        'idade': idade
    }
    print(tparams)
    return render(request, 'jogador.html', tparams)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def change(value):
    return value.replace("+"," ")
