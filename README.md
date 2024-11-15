## Bot Scrapper de notícias das Olimpíadas 2024

Esse bot visa o scrapping de 12 jornais do mundo inteiro. Sendo eles:

*    The Economist
*    Associated Press (AP)
*    The New York Times (NYTimes)
*    Rasmussen Reports
*    Detroit Free Press (Freep)
*    AZ Central
*    USA Today
*    Los Angeles Times (LA Times)
*    ABC News
*    PBS (Public Broadcasting Service)
*    New York Post (NY Post)
*    Las Vegas Review-Journal
*    NBC News
*    Fox News
*    Atlanta Journal-Constitution (AJC)

Este bot realiza o scraping de 15 jornais de renome mundial, verifica no banco de dados se a URL já foi processada para evitar duplicações e, caso não seja repetida, monta uma mensagem e a encaminha para o Telegram utilizando Python.

## Requisitos 

Crie um ambiente virtual para a execução e instalação das bibliotecas do projeto:
```
python3 -m venv venv
```
Ative o virtual enviroment em sua máquina:

* Windows
```
venv/Scripts/Activate.ps1
```
* MacOS/Linux:
```
source venv/bin/activate
```
Instalação das bibliotecas requisito do projeto:

```
pip install -r requirements.txt
```
## Execução

Para a criação de um bot, busque por Bot Father no Telegram e siga os passos para a criação do seu próprio bot. Certifique-se de ter preenchido main.py com suas informações de bot e grupo/chat de envio.
Execução do projeto:

```
python main.py
```

  
