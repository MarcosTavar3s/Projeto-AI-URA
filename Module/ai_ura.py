import re
import cv2
import time
import torch
import threading 
import numpy as np
import PIL.Image as Image
import paho.mqtt.client as mqtt
import google.generativeai as genai

from queue import Queue
from ultralytics import YOLO
from tello_zune import TelloZune


class AiUra():
    def __init__(self, esp_cam_address, yolo_drone_model, yolo_car_model, api_key, broker, mqtt_pub_topic, mqtt_sub_topic):
        # ESP32CAM
        self.esp_cam_address = esp_cam_address
        self.cap_esp_cam = cv2.VideoCapture(esp_cam_address)
        
        # MQTT
        self.broker = broker
        self.mqtt_pub_topic = mqtt_pub_topic
        self.mqtt_sub_topic = mqtt_sub_topic
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
        # Modelos do YOLO
        self.yolo_drone_model = YOLO(yolo_drone_model)
        self.yolo_car_model = YOLO(yolo_car_model)
        
        # Gemini
        generation_config = {
            "temperature": 0,
        }
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

        
        # Drone Tello
        # self.tello = TelloZune()
        
        # Inicia o Tello
        # self.tello.start_tello()
        
        # Fila para visualizacao
        self.visualizar = True
        
        self.frame_esp_cam = None
        self.queue = Queue()
        
        # Serie de movimentos que o carrinho tem que realizar para atingir a bolinha conforme a visao do drone
        self.serie_de_movimentos = ""
        
        
        # Inicializacao da variavel que vai servir para o processamento do YOLO a cada 2 segundos
        self.tempo_inicial = time.time()
        
        # Threads de processamento e captura de imagem
        self.thread_processamento = threading.Thread(target=self.processamento_imagem, daemon=True)
        self.thread_captura = threading.Thread(target=self.captura_imagens, daemon=True)
        self.thread_mqtt = threading.Thread(target=self.mqtt, daemon=True)
        
        # Inicio das threads
        self.thread_processamento.start()
        self.thread_captura.start()
        self.thread_mqtt.start()
        
        
    def captura_imagens(self):
        while self.visualizar:
            
            # Coleta a imagem da ESP32CAM
            ret_esp_cam, frame_esp_cam = self.cap_esp_cam.read()
            
            # Coleta a imagem do drone
            # self.frame_drone = self.tello.get_frame()
            self.frame_drone = cv2.imread('img teste/duas_caixas_reto.png')
            
            
            if not ret_esp_cam:
                print("Erro na abertura da ESP32CAM")
                break
            else:
                self.queue.put(frame_esp_cam)
            
            if not self.queue.empty():
                self.frame_esp_cam = self.queue.get()
            
        self.cap_esp_cam.release()
             
    def mostrar_imagens(self):
        while self.visualizar:
            
            if self.frame_esp_cam is not None:
                cv2.imshow("ESP32CAM", self.frame_esp_cam)
                cv2.imshow("Drone", self.frame_drone)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.visualizar = False
        self.disconnect()
        cv2.destroyAllWindows()
        
    def processamento_imagem(self):       
        while self.visualizar and self.serie_de_movimentos == "":     
            self.tempo_atual = time.time()
            
            # Processar a imagem com o YOLO a cada 2 segundos
            if self.tempo_atual - self.tempo_inicial >= 2:
                self.tempo_inicial = self.tempo_atual
            
                self.resultado_esp_cam = self.yolo_car_model(self.frame_esp_cam)
                
                self.boxes_esp_cam = self.resultado_esp_cam[0].boxes
                self.cls_esp_camp = self.boxes_esp_cam.cls
                
                # Bolinha identificada na ESP32CAM
                if tuple(self.cls_esp_camp.size())[0]:
                    # Coordenadas da bounding box
                    for box in self.boxes_esp_cam.xywh:
                        x,y,w,h = box
                        x,y,w,h = x.item(),y.item(),w.item(),h.item()
                        x,y,w,h = map(int, [x,y,w,h])

                
                # Bolinha nao foi identificada na ESP32CAM
                else: 
                    print('Nao identificada na ESP32CAM')

                    self.resultado_drone = self.yolo_drone_model(self.frame_drone)
                    
                    self.boxes_drone = self.resultado_drone[0].boxes
                    self.cls_drone = self.boxes_drone.cls
                                        
                    # Drone detectou o carrinho e a bolinha
                    if tuple(self.cls_drone.size())[0]:              

                        # Copia que sera colocada a bounding box
                        self.frame_drone_bb = self.frame_drone.copy()
                                               
                        for clse in self.cls_drone:
                            print(clse.item())
                         
                        # Desenho da bounding box
                        for box in self.boxes_drone.xywh:
                            x,y,w,h = box
                            x,y,w,h = x.item(),y.item(),w.item(),h.item()
                            x,y,w,h = map(int, [x,y,w,h])
                            cv2.rectangle(self.frame_drone_bb, (x-int(w/2),y-int(h/2)),(x+int(w/2),y+int(h/2)), (0,255,0), 3)
                        
                        self.gemini(self.frame_drone_bb)                    
        
    def gemini(self, img):
        # Se não houver uma serie de movimentos que devem ser executados, envie para o Gemini
        if self.serie_de_movimentos == "":
            cv2.imwrite('gemini.jpg', img)
            
            imagem_pil = Image.open('gemini.jpg')
            
            response = self.gemini_model.generate_content(["Existe um carrinho e uma bolinha na imagem. Determine qual movimentacao minima que o carrinho deve fazer para chegar a bolinha e nao colidir com os obstaculos que existem imediatamente em frente ao carrinho. Para cada movimento use os quadrados do piso para a referencia da movimentacao. Ao fim, retorne a resposta de forma sucinta: 'Va para a direita'==D, 'Va para a esquerda'==E, 'Va para a frente'==F, 'Va para tras'==T ate o carrinho atingir a bolinha. Descreva quantos quadrados do piso serao utilizados em cada movimento.", imagem_pil])

            self.serie_de_movimentos += response.text
                
            self.serie_de_movimentos = re.findall(r'[FEDT]\d{1}', self.serie_de_movimentos)
            # DEBUG: print(self.serie_de_movimentos)
            
            msg = ""
            
            for i in range(len(self.serie_de_movimentos)):
                if i != len(self.serie_de_movimentos) - 1:
                    msg += self.serie_de_movimentos[i] + "," 
                else:
                    msg += self.serie_de_movimentos[i] + "."   
            
            self.publish(msg)
        
        return                    
    
    def mqtt(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.client.connect(self.broker, 1883, 60)
        self.client.loop_forever()       

    def disconnect(self):
        print("Desconectando do broker...")
        self.client.disconnect()
        print("Broker finalizado")

    
    def on_connect(self, client, userdata, flags, rc, properties):
        print(f"Conectado ao broker com código de resultado {rc}")
        self.client.publish(self.mqtt_pub_topic, "MQTT conectado com sucesso")

        # Se inscrevendo no topico de escuta
        self.client.subscribe(self.mqtt_sub_topic)
        
    def on_message(client, userdata, msg):
        print(f'Mensagem de ${msg.topic}: ${msg.payload.decode()}')
        
    def publish(self, msg):
        self.client.publish(self.mqtt_pub_topic, msg)
