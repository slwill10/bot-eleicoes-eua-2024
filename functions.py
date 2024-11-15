import requests
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pymongo import InsertOne


def processar_termo(urls, base_url, termo):
    search_url = base_url + termo.replace(" ", "+")
    func = urls[base_url]
    return func(search_url)


def atualizar_mongo_cache(mongo, manchetes_local):
    requests = []
    for manchete in manchetes_local:
        requests.append(InsertOne(manchete))
    if requests:
        mongo.db.collection.bulk_write(requests)


def enviar_mensagem(token, chat_id, mensagem):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': mensagem
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Mensagem enviada com sucesso para o chat_id {chat_id}")
        else:
            print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Exceção ao enviar mensagem: {e}")

def economist(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            headline_tags = soup.find_all('div', class_='css-1ejiw6s e17qp5ds0')

            print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    span_tag = tag.find('span', class_='_headline')
                    headlines.append({'texto': span_tag.get_text(strip=True), 'fonte': link_tag['href']})

            print(headlines)
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e: 
        print(f'Ocorreu um erro com {url}: {e}')

    return headlines

def ny_times(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headline_tags = soup.find_all('li', class_='css-1l4w6pd')
            print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    span_tag = tag.find('h4', class_='css-nsjm9t')
                    headlines.append({'texto': span_tag.get_text(strip=True), 'fonte': f'https://www.nytimes.com{link_tag['href']}'})
            
            print(headlines)

        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e: 
        print(f'Ocorreu um erro com {url}: {e}')

    return headlines

def rasmussenreports(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headline_tags = soup.find_all('div', class_='search-line d-flex align-items-start')

            print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    title_tag = tag.find('h3', class_='mt-1 mb-2')
                    headlines.append({'texto': title_tag.get_text(strip=True), 'fonte': f'https://www.rasmussenreports.com{link_tag['href']}'})
            print(headlines)

        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e: 
        print(f'Ocorreu um erro com {url}: {e}')

    return headlines

def latimes(url):
    headlines = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                headline_tags = soup.find_all('div', class_='promo-wrapper')

                print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

                for tag in headline_tags:
                    link_tag = tag.find('a')
                    if link_tag:
                        title_tag = tag.find('h3', class_='promo-title')
                        headlines.append({'texto': title_tag.get_text(strip=True), 'fonte': link_tag['href']})
                print(headlines)
                
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e:    
        print(e)

    return headlines

def freep(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headline_tags = soup.find_all('a', class_='gnt_se_a gnt_se_a__hd gnt_se_a__hi')

            print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

            for tag in headline_tags:
                headlines.append({'texto': tag.get_text(strip=True), 'fonte': f'https://www.freep.com{tag['href']}'})

            print(headlines)
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e: 
        print(f'Ocorreu um erro com {url}: {e}')

    return headlines

def azcentral(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headline_tags = soup.find_all('a', class_='gnt_se_a gnt_se_a__hd gnt_se_a__hi')

            print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

            for tag in headline_tags:
                headlines.append({'texto': tag.get_text(strip=True), 'fonte': f'https://www.azcentral.com{tag['href']}'})

            print(headlines)
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e: 
        print(f'Ocorreu um erro com {url}: {e}')

    return headlines

def usatoday(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headline_tags = soup.find_all('a', class_='gnt_se_a gnt_se_a__hd gnt_se_a__hi')

            print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

            for tag in headline_tags:
                headlines.append({'texto': tag.get_text(strip=True), 'fonte': f'https://www.usatoday.com{tag['href']}'})
            print(headlines)

        else:
            print(f"Erro ao acessar {url}: {response.status_code}")

    except Exception as e: 
        print(f'Ocorreu um erro com {url}: {e}')

    return headlines

def abc_news(url):
    headlines = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)
            page.wait_for_load_state('networkidle')

            page_content = page.content()
            soup = BeautifulSoup(page_content, 'html.parser')
            headline_tags = soup.find_all('section', class_='ContentRoll__Item')
            print(f"Encontradas {len(headline_tags)} manchetes. url: {url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    headlines.append({
                        'texto': link_tag.get_text(strip=True),
                        'fonte': link_tag['href']
                    })

            browser.close()
            print(headlines)

    except Exception as e:
        print(f"Erro durante a extração: {e}")

    return headlines     

def fox_news(url):
    headlines = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, timeout=120000)
            page.wait_for_load_state('networkidle', timeout=120000)
            time.sleep(10)

            page_content = page.content()
            soup = BeautifulSoup(page_content, 'html.parser')

            headline_tags = soup.find_all('article', class_='article')
            print(f"Encontradas {len(headline_tags)} manchetes. url: {url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    title_tag = tag.find('h2', class_='title')
                    if title_tag:
                        headlines.append({
                            'texto': title_tag.get_text(strip=True),
                            'fonte': link_tag['href']
                        })

            browser.close()
            print(headlines)

    except Exception as e:
        print(f"Erro durante a extração: {e}")

    return headlines  

def pbs(url):
    headlines = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)
            page.wait_for_load_state('networkidle')
            page_content = page.content()

            soup = BeautifulSoup(page_content, 'html.parser')
            headline_tags = soup.find_all('li', class_='search-result-video-item')
            print(f"Encontradas {len(headline_tags)} manchetes. url: {url}")

            for tag in headline_tags:
                link_tag = tag.find('a', class_='search-result-video-item__video-title')
                if link_tag:
                    headlines.append({
                        'texto': link_tag.get_text(strip=True),
                        'fonte': f"https://www.pbs.org{link_tag['href']}"
                    })

            browser.close()
            print(headlines)

    except Exception as e:
        print(f"Erro durante a extração: {e}")

    return headlines

def ny_post(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                headline_tags = soup.find_all('div', class_='search-results__story')

                print(f"Encontradas {len(headline_tags)} manchetes.url:{url}")

                for tag in headline_tags:
                    link_tag = tag.find('a')
                    if link_tag:
                        title_tag = tag.find('h3', class_='story__headline headline headline--archive')  
                        headlines.append({'texto': title_tag.get_text(strip=True), 'fonte': link_tag['href']})
                print(headlines)

    except Exception as e:    
        print(e)  

    return headlines    

def ajc(url):
    headlines = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, timeout=120000)
            page.wait_for_load_state('networkidle', timeout=120000)

            page_content = page.content()
            soup = BeautifulSoup(page_content, 'html.parser')
            headline_tags = soup.find_all('div', class_='queryly_item_row')
            print(f"Encontradas {len(headline_tags)} manchetes. url: {url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    title_tag = tag.find('div', class_='queryly_item_title')
                    if title_tag:
                        headlines.append({
                            'texto': title_tag.get_text(strip=True),
                            'fonte': f"https://www.ajc.com{link_tag['href']}"
                        })

            browser.close()
            print(headlines)

    except Exception as e:
        print(f"Erro durante a extração: {e}")

    return headlines

def review_journal(url):
    headlines = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                headline_tags = soup.find_all('div', class_='field-col right')

                print(f"Encontradas {len(headline_tags)} manchetes. url:{url}")

                for tag in headline_tags:
                    link_tag = tag.find('a')
                    if link_tag:
                        headlines.append({'texto': link_tag.get_text(strip=True), 'fonte': link_tag['href']})

                print(headlines)
    except Exception as e:    
        print(e) 

    return headlines  

def nbc_news(url):
    headlines = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)
            page.wait_for_load_state('networkidle')

            page_content = page.content()
            soup = BeautifulSoup(page_content, 'html.parser')
            headline_tags = soup.find_all('div', class_='gsc-webResult gsc-result')
            print(f"Encontradas {len(headline_tags)} manchetes na URL: {url}")

            for tag in headline_tags:
                link_tag = tag.find('a')
                if link_tag:
                    headlines.append({'texto': link_tag.get_text(strip=True), 'fonte': link_tag['href']})

            browser.close()
            print(headlines)

    except Exception as e:
        print(f"Erro durante a extração: {e}")

    return headlines

def ap_org(url):
    header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
    response = requests.get(url, headers=header, timeout=300)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    manchetes = []
        
    for tag in soup.find_all('a', class_='grid-card grid-card__post'):
        h3_tag = tag.find('h3', class_='grid-card__page-title h6')
        a_tag = tag['href']
        manchetes.append({'texto': h3_tag.get_text(strip=True), 'fonte': a_tag})

    return manchetes