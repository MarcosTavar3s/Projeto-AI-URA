import re
import cv2
import time
import torch
import threading 
import numpy as np
import PIL.Image as Image
import google.generativeai as genai

from queue import Queue
from ultralytics import YOLO
from tello_zune import TelloZune


class AiUra():
    def __init__(self, esp_cam_address, yolo_drone_model, yolo_car_model, api_key):
        # Ip da camera
        self.esp_cam_address = esp_cam_address
        self.cap_esp_cam = cv2.VideoCapture(0)
        
        # Modelos 
        self.yolo_drone_model = YOLO(yolo_drone_model)
        self.yolo_car_model = YOLO(yolo_car_model)
        
        # Gemini
        generation_config = {
            "temperature": 0,
        }
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

        
        # Objeto TelloZune
        # self.tello = TelloZune()
        
        # Inicia o Tello
        # self.tello.start_tello()
        
        self.visualizar = True
        
        self.frame_esp_cam = None
        self.queue = Queue()
        
        # Serie de movimentos que o carrinho tem que realizar para atingir a bolinha conforme a visao do drone
        self.serie_de_movimentos = ""
        
        
        # Inicializacao da variavel que vai servir para o processamento a cada 2 segundos
        self.tempo_inicial = time.time()
        
        # Threads de processamento e captura de imagem
        self.thread_processamento = threading.Thread(target=self.processamento_imagem, daemon=True)
        self.thread_captura = threading.Thread(target=self.captura_imagens, daemon=True)
        
        # Inicio das threads
        self.thread_processamento.start()
        self.thread_captura.start()
        
        
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
            
            response = self.gemini_model.generate_content(["Existe um carrinho e uma bolinha na imagem. Determine qual movimentacao minima que o carrinho deve fazer para chegar a bolinha e nao colidir com os obstaculos que existem imediatamente em frente ao carrinho. Para cada movimento use os quadrados do piso para a referencia da movimentacao. Ao fim, retorne a resposta de forma sucinta: 'Va para a direita'==D, 'Va para a esquerda'==E, 'Va para a frente'==F, 'Va para tras'==T ate o carrinho atingir a bolinha. Descreva quantos quadrados do piso serao utilizados em cada movimento.", imagem_pil], stream=True)

            for chunk in response:
                self.serie_de_movimentos += chunk.text
                
            self.serie_de_movimentos = re.findall(r'[FEDT]\d{1}', self.serie_de_movimentos)
            print(self.serie_de_movimentos)
        
        return                    
      

    

