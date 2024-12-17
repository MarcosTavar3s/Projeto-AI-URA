from tello_zune import TelloZune
from ultralytics import YOLO
import numpy as np
import cv2
import torch
import time

# tello = TelloZune()
# tello.start_tello()

model_esp = YOLO('Database/best.pt')
model_drone = YOLO('Database/best.pt')

drone_cam = cv2.VideoCapture(0)
esp_cam = cv2.VideoCapture("http://10.6.3.68:81/stream")

empty_array = np.array([])

def id_yolo(img: np.ndarray, height: int, width: int, model: YOLO) -> np.ndarray:
    """
    Analisa a imagem recebida no modelo do YOLO 
    
    Args:
		img (np.ndaarray): imagem a ser processada
		height (int): altura da imagem
		width (int): largura da imagem
		model (YOLO): modelo do YOLO
		
	Return:
		np.ndarray: de tamanho 0 se não for identificado, imagem se for identificado
    """
    
    # Variáveis dos retângulos de referência
    bwRect1 = int(0.3*width)
    ewRect1 = int(0.7*width)
    bhRect2 = int(0.3*height)
    ehRect2 = int(0.7*height)
    
    # Processamento da imagem
    result = model(img)
    res = result[0].boxes
    
    if not len(res.xywh):
        print('Bolas não detectadas')
        return empty_array
    
    else:
        # Quantidade de bounding boxes detectadas == Quantidade de objetos detectados
        size = len(res.xywh)
        
        boxesxywh = res.xywh
        boxesxyxy = res.xyxy   
        
        # Confiabilidade da previsão
        conf = res.conf
        
        # Bola com maior confiabilidade 
        i = torch.argmax(conf)       
        
        # Coordenadas da bola com maior confiabilidade
        x,y,w,h = boxesxywh[i]
        cv2.putText(img, str(h.item()), (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
        
        # Movimentação do Tello
        if x > bwRect1 and x < ewRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x < bwRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'esquerda - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x > ewRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'direita - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x > bwRect1 and x < ewRect1 and y < bhRect2:
                cv2.putText(img, 'em cima - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x > bwRect1 and x < ewRect1 and y > ehRect2:
                cv2.putText(img, 'embaixo - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x < bwRect1 and y < bhRect2: 
                cv2.putText(img, 'em cima - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x < bwRect1 and y > ehRect2: 
                cv2.putText(img, 'embaixo - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x > ewRect1 and y < bhRect2: 
                cv2.putText(img, 'em cima - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        elif x > ewRect1 and y > ehRect2: 
                cv2.putText(img, 'embaixo - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                
        # alterei o 0 no index por i
        upperBorderX, upperBorderY, downBorderX, downBorderY = boxesxyxy[i]
        upperBorderX, upperBorderY, downBorderX, downBorderY = map(int, [upperBorderX, upperBorderY, downBorderX, downBorderY])
        
        cv2.rectangle(img,(upperBorderX,upperBorderY), (downBorderX, downBorderY), (0,255,0),3)
        
        # Centro de massa da bolinha
        cv2.rectangle(img, (int(x),int(y)), (int(x),int(y)), (0,255,255),3)
    
        # Vetor de direção em relação ao centro da imagem
        cv2.arrowedLine(img, (int(width/2),int(height/2)), (int(x),int(y)), (255,0,0), 2)
    
    return img

def main():
    # Inicia abrindo a camera da ESP32 para
    _, frame_esp = esp_cam.read()
    cv2.imshow('Processamento de imagem - ESP32CAM', frame_esp)
    
    _, frame_drone = drone_cam.read()
    cv2.imshow('Processamento de imagem - Drone', frame_drone) 
        
    while True:
        ret, frame_esp = esp_cam.read()
        ret, frame_drone = drone_cam.read() # tello.get_frame()

        height_esp, width_esp, _ = frame_esp.shape
        height_drone, width_drone, _ = frame_drone.shape

        identified_esp = False
        
        if not ret:
            break
            
        imgYolo_esp = id_yolo(frame_esp, height_esp, width_esp, model_esp)

        if imgYolo_esp.size:
            frame_esp = imgYolo_esp 
            identified_esp = True
        
        if not identified_esp:
            imgYolo_drone = id_yolo(frame_drone, height_drone, width_drone, model_drone)

            if imgYolo_drone.size:
                frame_drone = imgYolo_drone
        
        cv2.imshow('Processamento de imagem - ESP32CAM', frame_esp)
        cv2.imshow('Processamento de imagem - Drone', frame_drone)

        
        if cv2.waitKey(1) & 0xFF == 27:
            break


cv2.destroyAllWindows()

if __name__ == "__main__":
        main()
