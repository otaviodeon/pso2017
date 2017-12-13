import requests
import sys
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup

def le_entrada(e):
    if (len(e) < 2):
        print("Digite o assunto a ser buscado.")
        return False
    elif (len(e) == 4):
        if (e[2] == '-d'):
            return [e[1], e[3]]             #retorna o termo de pesquisa e a data minima das publicacoes
    else:
        return [e[1]]                     #retorna apenas o termo de pesquisa


def monta_resultado(r):
    with open('results.html', 'w') as p:
        p.write(r)

### RETORNA RESULTADOS DA PESQUISA NUM DICIONARIO COM LISTAS DO TIPO [TITULO, LINK, DATA DE PUBLICACAO]
def guarda_resultado(c):
    resultados = {}

    cont = 0
    for r in c['results']:
        item = [r['webTitle'], r['webUrl'], r['webPublicationDate']]
        resultados[cont] = item
        cont = cont + 1

    return resultados

### ABRE LINK DE CADA NOTICIA, PEGA SOMENTE O CONTEUDO E MONTA O ARQUIVO HTML
def abre_resultado(r, assunto):
    html = '<html><head><title>Noticias Guardian</title></head><body>'
    html += '<center><h1>' + assunto + '</h1></center>'

    for k, v in r.items():
        request = requests.get(v[1])
        soup = BeautifulSoup(request.content, 'html.parser')
        corpoNoticia = soup.findAll("div", itemprop="articleBody")      #filtra div que contem o conteudo da noticia
        if (not corpoNoticia):
            corpoNoticia = soup.findAll("div", itemprop="reviewBody")   #caso seja categoria review em vez de article
        if (not corpoNoticia):
            continue

        data = datetime.strptime(v[2][:10], '%Y-%m-%d')
        dataFormatada = "{:%d/%m/%Y}".format(data)
        html += '<center><h2><a href="' + v[1] + '">' + v[0].encode('ascii', 'xmlcharrefreplace') + '</a></h2>'
        html += '<h4>' + str(dataFormatada) + '</center>'

        corpo = ''
        for i in corpoNoticia:
            corpo = i.find_all('p')         #pega so conteudo dentro das tags <p>
            for c in corpo:
                html += c.text.encode('ascii', 'xmlcharrefreplace')
                html += "<br><br>"
        html += '<hr>'

    html += '</body></html>'
    monta_resultado(html)


def main():
    busca = le_entrada(sys.argv)
    if (busca == False):
        return 0
    print ("Buscando...")

    if (len(busca) == 1):
        url = 'http://content.guardianapis.com/search?order-by=newest&api-key=7a08c584-4fff-4c52-9600-ec5cc0a6b197&q=' + busca[0]
    elif (len(busca) == 2):
        dataMinima = datetime.strptime(busca[1], '%Y-%m-%d')
        dataMinima = dataMinima.strftime('%Y-%m-%d')
        url = 'http://content.guardianapis.com/search?order-by=newest&from-date=' + str(dataMinima) + '&api-key=7a08c584-4fff-4c52-9600-ec5cc0a6b197&q=' + busca[0]
    request = requests.get(url)
    c = request.json()['response']
    if (c['total'] == 0):
        monta_resultado("<h1>Nenhum resultado foi achado. Tente buscar com outros termos.</h1>")
        return 0

    resultados = guarda_resultado(c)
    abre_resultado(resultados, busca[0])

    url = "results.html"
    webbrowser.open(url)

main()
