from tello_zune.examples.tello_zune import TelloZune
from ultralytics import YOLO
import numpy as np
import cv2
import torch
import time

# Caminho do modelo treinado
path =''

# Importação do modelo
model = YOLO(path)

# Cria objeto do TelloZune
tello = TelloZune()

def idYolo(img, height, width):
    
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
                # tello.move_forward(20)
        elif x < bwRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'esquerda - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.rotate_counter_clockwise(15)
        elif x > ewRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'direita - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.rotate_clockwise(15)
        elif x > bwRect1 and x < ewRect1 and y < bhRect2:
                cv2.putText(img, 'em cima - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.move_up(20)
        elif x > bwRect1 and x < ewRect1 and y > ehRect2:
                cv2.putText(img, 'embaixo - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.move_down(20)
        elif x < bwRect1 and y < bhRect2: 
                cv2.putText(img, 'em cima - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.move_up(20)
                # tello.rotate_counter_clockwise(15)         
        elif x < bwRect1 and y > ehRect2: 
                cv2.putText(img, 'embaixo - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.move_up()
                # tello.rotate_counter_clockwise(15)
        elif x > ewRect1 and y < bhRect2: 
                cv2.putText(img, 'em cima - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.move_up(20)
                # tello.rotate_clockwise(15)            
        elif x > ewRect1 and y > ehRect2: 
                cv2.putText(img, 'embaixo - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                # tello.move_down(20)
                # tello.rotate_clockwise(15)
                
        upperBorderX, upperBorderY, downBorderX, downBorderY = boxesxyxy[0]
        upperBorderX, upperBorderY, downBorderX, downBorderY = map(int, [upperBorderX, upperBorderY, downBorderX, downBorderY])
        
        cv2.rectangle(img,(upperBorderX,upperBorderY), (downBorderX, downBorderY), (0,255,0),3)
        
        # Centro de massa da bolinha
        cv2.rectangle(img, (int(x),int(y)), (int(x),int(y)), (0,255,255),3)
    
        # Vetor de direção em relação ao centro da imagem
        cv2.arrowedLine(img, (int(width/2),int(height/2)), (int(x),int(y)), (255,0,0), 2)
    
    return img

def main():
    # Inicia o Tello
    tello.start_tello()
    
    
    while True:
        img = tello.get_frame()
        
        height, width, _ = img.shape
        
        cv2.imshow('pre-processamento',img)        
        imgYolo = idYolo(img, height, width)    
        
        cv2.imshow('yolo',imgYolo)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    
    tello.end_tello()
    cv2.destroyAllWindows()

if __name__ == "__main__":
 main()
