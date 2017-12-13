Trabalho final de Práticas de SO

Descrição: Utilizando a API de busca de publicações do site do jornal inglês The Guardian, o programa retorna até 10 notícias (articles e reviews) relacionadas ao assunto que o usuário der como entrada.
Para lidar com o conteúdo, foram utilizadas as bibliotecas requests e BeautifulSoup (parser HTML).
Execute com o comando "python t6-odeon.py <assunto>".
Ou, se desejar filtrar os resultados por data mínima de publicação, execute "python t6-odeon.py -d <data>", com a data no formato YYYY-MM-DD.
Os resultados são montados numa página simples html que é aberta automaticamente em um navegador no fim da execução do programa.

Referências:
API do jornal The Guardian: http://open-platform.theguardian.com/
