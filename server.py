from flask import Flask
from flask_socketio import SocketIO,emit,send
from bs4 import BeautifulSoup
from selenium import webdriver   #its the library
import time
 
#First we create call the Flask framework and create a secret password.
#Then create socketio variable where cors_allowed_origin = * to acept communication with other domains.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

url = 'https://plenamata.eco/monitor/'
driver.get(url)
 
#This is the function that will create the Server in the ip host and port 5000
if __name__ == "__main__":
    print("starting webservice")
 
 
#Function that runs when a clients get connected to the server
@socketio.on('connect')
def test_connect():
    print('Client connected test')
    emit('my response', {'data': 'Connected1'},broadcast=True)

#Read data from client
@socketio.on('new-message')
def handle_message(message):
    time.sleep(5)
    websraping()

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
 
def websraping():
    html = driver.page_source
    page_soup = BeautifulSoup(html,features="lxml")

    dados_roubados = page_soup.findAll("span", {"class": "dashboard-panel__number"})
    # print(dados_roubados)
    emit('my response',  {
        "arvoresCortadas": dados_roubados[0].text,
        "desmatamentoTotal": dados_roubados[1].text,
        "taxaDesmatamentoDia": dados_roubados[2].text,
        "taxaDesmatamentoHec": dados_roubados[3].text,
        "areaDesmatada": dados_roubados[4].text,
        
    })


