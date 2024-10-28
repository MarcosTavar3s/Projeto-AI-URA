# Importação das bibliotecas
from ultralytics import YOLO
import cv2
import numpy as np
from threading import Thread
import torch
import paho.mqtt.client as mqtt

# Caminho do modelo
path ='/'

# Carregando o modelo
model = YOLO(path)

client = mqtt.Client()

# Conexão do MQTT
def on_connect(client, userdata, flags, rc):
    # Conectando ao broker
    print(f"Conectado ao broker com código de resultado {rc}")
    
    global disconnectMqtt
    disconnectMqtt = False
    
    # Publicando no tópico 
    client.publish('aiurarecebe', 'MQTT conectado')

# Impressão da mensagem recebida pelo tópico 
def on_message(client, userdata, msg):
    print(f'Mensagem de ${msg.topic}: ${msg.payload.decode()}')

# Desconectar do broker
def disconnect():
    global client
    print('Encerrando conexão com o broker...')
    client.disconnect()
    print('Conexão com o broker encerrada')

# Publicar mensagem no broker
def publish(msg):
    global client
    client.publish('aiurarecebe', msg)

# Função principal do MQTT
def mqttEsp():    
    global mqttMessage
    global client

    client.on_connect = on_connect
    client.on_message = on_message
    
    broker = 'broker.emqx.io'
    client.connect(broker, 1883, 60)
    
    client.loop_forever()       

# Função principal do processamento da imagem pelo YOLO
def idYolo(img):
    result = model(img)
    height, width , _ = img.shape
    
    bwRect1 = int(0.3*width)
    ewRect1 = int(0.7*width)
    
    res = result[0].boxes    
    if len(res.xywh):
    
        # Caixas
        boxesxywh = res.xywh
        boxesxyxy = res.xyxy
        
        # Confiabilidade da previsão
        conf = result[0].boxes.conf
        i = torch.argmax(conf)       

        x,y,w,h = boxesxywh[i]
        
        upperBorderX, upperBorderY, downBorderX, downBorderY = boxesxyxy[i]
        upperBorderX, upperBorderY, downBorderX, downBorderY = map(int, [upperBorderX, upperBorderY, downBorderX, downBorderY])
        
        cv2.rectangle(img,(upperBorderX,upperBorderY), (downBorderX, downBorderY), (0,255,0),3)
        
        if x >= bwRect1 and x <= ewRect1:
            cv2.putText(img, 'Frente', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)
            publish('F')
        elif x < bwRect1:
            cv2.putText(img, 'Direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)
            publish('D')
        elif x > ewRect1:
            cv2.putText(img, 'Esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)
            publish('E')
        else:
            cv2.putText(img, 'Parado', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)
            publish('P')
        
    else:
         publish('0 bola(s) encontrada(s)')
         publish('P')

    # Retângulo que divide a tela em 3
    cv2.rectangle(img,(bwRect1,0),(ewRect1,height),(255,0,0),4)
    return img

# Função para mostrar a camera do drone
def mostraImagem():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print('Erro em abrir a camera')
            break
        
        if cv2.waitKey(1) & 0xff == 27:
            break
        
        cv2.imshow('frame', frame)
        img = idYolo(frame)
        cv2.imshow('YOLO', img)

    cap.release()
    disconnect()
    cv2.destroyAllWindows()

# Função principal
def main():
    # Cria as Threads
    imagem = Thread(target=mostraImagem)
    comunicacao = Thread(target=mqttEsp)
    
    # Inicia os processos
    imagem.start()
    comunicacao.start()
    
    # Aguarda a conclusão dos processos
    imagem.join()
    comunicacao.join()

if __name__ == '__main__':
    main()
