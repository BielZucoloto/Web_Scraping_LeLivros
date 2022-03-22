import requests
from bs4 import BeautifulSoup
import json

minha_lista = {}
livros_json = []

autor = input('Digite o autor que deseja pesquisar: ')
autor_formatado = autor.lower().replace(' ','+')
url = (f'https://lelivros.love/?x=0&y=0&s={autor_formatado}')

pagina = requests.get(url)
soup = BeautifulSoup(pagina.content, "html.parser")
find_by_class = soup.find_all(class_="post-17105 product type-product status-publish has-post-thumbnail hentry first instock")
contador = 0
for h in find_by_class:
    contador = contador + 1
    tag_h3 = h.find('h3')
    tag_a = h.find('a')
    if 'href' in tag_a.attrs:
        link = tag_a.get('href')
        minha_lista[contador] = str(link)
        livros_json.append(['ID',str(contador),'TITULO',str(tag_h3).replace('<h3>','').replace('</h3>','').strip()])
        print (f'\n{contador})',str(tag_h3).replace('<h3>','').replace('</h3>','').strip())


for y in range(50):
    y = y + 2
    url_pagina = (f'https://lelivros.love/page/{y}/?x=0&y=0&s={autor_formatado}')
    url_status = requests.post(url_pagina)
    url_status_code = (url_status.status_code) #200 ou 404
    if url_status_code == 200:
        pagina = requests.get(url_pagina)
        soup = BeautifulSoup(pagina.content, "html.parser")
        find_by_class = soup.find_all(class_="post-17105 product type-product status-publish has-post-thumbnail hentry first instock")
        for h in find_by_class:
            contador = contador + 1
            tag_h3 = h.find('h3')
            tag_a = h.find('a')
            if 'href' in tag_a.attrs:
                link = tag_a.get('href')
                minha_lista[contador] = str(link)
                livros_json.append(['ID',str(contador),'TITULO',str(tag_h3).replace('<h3>','').replace('</h3>','').strip()])
                print (f'\n{contador})',str(tag_h3).replace('<h3>','').replace('</h3>','').strip())
    else:
        break

link_epub = None
link_pdf = None
link_mobi = None
link_online = None

tamanho_livros = (len(livros_json))
tamanho_livros_contador = 0

meus_links = {}
for item in minha_lista:
    url = (minha_lista[item])
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content, "html.parser")
    find_by_class = soup.find_all("div", {"class": "links-download"})
    for h in find_by_class:
        for a in h.find_all('a'):
            if link_epub == None:
                link_epub = a.get('href')
            elif link_pdf == None:
                link_pdf = a.get('href')
            elif link_mobi == None:
                link_mobi = a.get('href')
            elif link_online == None:
                link_online = a.get('href')
        
        if tamanho_livros_contador <= tamanho_livros:
            for id in livros_json[tamanho_livros_contador]:
                livros_json[tamanho_livros_contador].append('EPUB')
                livros_json[tamanho_livros_contador].append(link_epub)

                livros_json[tamanho_livros_contador].append('PDF')
                livros_json[tamanho_livros_contador].append(link_pdf)

                livros_json[tamanho_livros_contador].append('MOBI')
                livros_json[tamanho_livros_contador].append(link_mobi)

                livros_json[tamanho_livros_contador].append('ONLINE')
                livros_json[tamanho_livros_contador].append(link_online)

                link_epub = None
                link_pdf = None
                link_mobi = None
                link_online = None

                tamanho_livros_contador = tamanho_livros_contador + 1
                
                break

print('\n\n')
for kkk in range(len(livros_json)):
    print(livros_json[kkk],'\n')
print('\n\n')

     
print (json.dumps(livros_json,ensure_ascii=False, indent = 1))