from ultralytics import YOLO
import cv2
import numpy as np
import cv2
import torch
import time
from tello_zune.examples.tello_zune import TelloZune

model = YOLO('best.pt')

tello = TelloZune()
tello.start_tello()

def idYolo(img, height, width):
    
    # Variáveis dos retângulos de referência
    bwRect1 = int(0.3*width)
    ewRect1 = int(0.7*width)
    bhRect2 = int(0.3*height)
    ehRect2 = int(0.7*height)
    
    result = model(img)
    img = result[0].plot()


    # Desenho dos retângulos na tela - referência    
    cv2.rectangle(img, (bwRect1, 0), (ewRect1, height), (0,255,0), 2)    
    cv2.rectangle(img, (0, bhRect2), (width, ehRect2), (0,255,0), 2) 
    

    if not len(result[0].boxes.xywh):
        print('Bolas não detectadas')
    
    else:
        # Quantidade de bounding boxes detectadas == Quantidade de objetos detectados
        size = len(result[0].boxes.xywh)
        
        boxesxywh = result[0].boxes.xywh
        print(result[0].boxes.conf)    
        
        # Confiabilidade da previsão
        conf = result[0].boxes.conf
        
        # Bola com maior confiabilidade 
        i = torch.argmax(conf)       
        
        # Coordenadas da bola com maior confiabilidade
        x,y,w,h = boxesxywh[i]
        cv2.putText(img, str(h.item()), (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
        
        # if h.item() < 50: ##COLOCAR PARAMETRO ADEQUADO DE DISTANCIA (D_mínima)
        #     cv2.putText(img, 'bolinha identificada - distancia minima atingida', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
        # else:
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
                
                

        
        # Centro de massa da bolinha
        cv2.rectangle(img, (int(x),int(y)), (int(x),int(y)), (0,255,255),3)
        
        # Vetor de direção em relação ao centro da imagem
        cv2.arrowedLine(img, (int(width/2),int(height/2)), (int(x),int(y)), (255,0,0), 2)
    
    return img

def main():
 # Inicia o stream de vídeo
 time.sleep(2)
 
#  tello.takeoff()
 
 while True:
    # Captura e processamento contínuo do drone
    while True:
        img = tello.get_frame()  # Captura o frame do drone
        tello.calc_fps(img)      # Calcula o FPS (Frames por segundo)

        cv2.imshow('Tello', img)  # Mostra o frame em uma janela chamada 'Tello'

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Se pressionar 'q', sai do loop
            break

    # Após sair do loop interno, redimensiona e processa a imagem com YOLO
    resized_img = cv2.resize(img, (480, 369))  # Redimensiona a imagem
    img = idYolo(resized_img, 369, 480)        # Passa a imagem redimensionada para o YOLO

    # Mostra o resultado da imagem processada
    cv2.imshow("drone", img)

    # Verifica se a tecla 'ESC' foi pressionada, se sim, sai do loop principal
    if cv2.waitKey(1) & 0xff == 27:  # ESC para sair
        break

# Limpeza final
cv2.destroyAllWindows()

 

if __name__ == "__main__":
 main()
