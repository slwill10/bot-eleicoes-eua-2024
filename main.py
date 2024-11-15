from functions import *
from connection import *
from datetime import datetime
import concurrent.futures


telegram_token = 'SEU_TOKEN'
mongo = MonogoDB('SEU_BANCO')

id_bot = 'SEU_ID'

urls = {
    "https://www.economist.com/search?q=": economist,
    "https://www.ap.org/?s=": ap_org,
    "https://www.nytimes.com/search?query=": ny_times,
    "https://www.rasmussenreports.com/search?SearchText=": rasmussenreports,
    "https://www.freep.com/search/?q=": freep,
    "https://www.azcentral.com/search/?q=": azcentral,
    "https://www.usatoday.com/search/?q=": usatoday,
    "https://www.latimes.com/search?q=": latimes, 
    "https://abcnews.go.com/search?searchtext=": abc_news,
    "https://www.pbs.org/search/?q=": pbs,
    "https://nypost.com/search/": ny_post,
    "https://www.reviewjournal.com/?s=": review_journal,
    "https://www.nbcnews.com/search/?q=" : nbc_news,
    "https://www.foxnews.com/search-results/search?q=": fox_news,
    "https://www.ajc.com/search/?q=": ajc,
}

termos = [
    "Kamala", "Trump", "Biden",
    "Presidential race", "Presidential election", "Poll", "Gallup", "Ipsos", "Morning Consult",
    "YouGov", "Elections in the United States", "Vance", "Tim Walz"
]


def main():

    start_time = time.time()

    # diminui o numero de threads, o numero anterior o gpt falou que poderia estar sobrecarregando
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    
    # 1 - Percorre termo por termo
    for termo in termos:
        manchetes_local = [] 

    # 2 - Aqui que processa em multithread as urls com os termos.
        futures = [executor.submit(processar_termo, urls, base_url, termo) for base_url in urls]
        for future in concurrent.futures.as_completed(futures):
            resultado = future.result()
            if resultado:
                manchetes_local.extend(resultado) 

        if manchetes_local: 
            mensagens_para_enviar = [] 
            atualizar_mongo_cache(mongo, manchetes_local)  

        # 3 - Aqui fizemos um multithread para adicionar as noticias na variável mensagens_para_enviar.
            for manchete in manchetes_local:
                if '_id' in manchete:
                    del manchete['_id']
                if 'fonte' in manchete:
                    if 'fonte' in manchete and manchete['fonte'] and 'texto' in manchete and manchete['texto']:
                        manchete['fonte'] = manchete['fonte'].split('?')[0]  # Normaliza a fonte
                        future = executor.submit(mongo.find_one_and_update, 'ws', manchete)
                if future.result() is None:
                    mensagens_para_enviar.append(
                        f"{manchete['texto']}\nFonte: {manchete['fonte']}\n" 
                    )
            # 4 - pegas as manchetes da variável mensagens_para_enviar, monta a mensagem e envia em lotes.
            batch_size = 15  
            if mensagens_para_enviar:  
                now = datetime.now()
                date_time = now.strftime("%d/%m às %H:%M:%S")

                for i in range(0, len(mensagens_para_enviar), batch_size):
                    batch_mensagens = mensagens_para_enviar[i:i + batch_size]
                    message_lines = [f"{mensagem}" for mensagem in batch_mensagens]
                    message = (f"📢 Últimas notícias do Bot Eleições EUA! 🇺🇸\n"
                            f"Data de extração: {date_time}\n"
                            f"Termo: {termo}\n\n" + "\n".join(message_lines))  
                    
                    time.sleep(1)  
                    executor.submit(enviar_mensagem, telegram_token, id_bot, message)

    executor.shutdown(wait=True)

    end_time = time.time()

    print(f'Tempo total de execucao: {(end_time - start_time) / 60} segundos')

if __name__ == "__main__":
    main()