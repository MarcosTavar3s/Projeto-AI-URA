from djitellopy import Tello
from ultralytics import YOLO
import cv2
import numpy as np
import cv2
import torch
import time

model = YOLO('YOLO Treinado/runs/detect/train3/weights/best.pt')

tello = Tello()
tello.connect()
        
battery_level = tello.get_battery()

print(f'Nível:{battery_level}')

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
         #     tello.send_rc_control(0,0,0,0)
        #     cv2.putText(img, 'bolinha identificada - distancia minima atingida', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
        # else:
        if x > bwRect1 and x < ewRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_forward(20)
        elif x < bwRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'esquerda - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.rotate_counter_clockwise(15)
        elif x > ewRect1 and y > bhRect2 and y < ehRect2:
                cv2.putText(img, 'direita - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.rotate_clockwise(15)
        elif x > bwRect1 and x < ewRect1 and y < bhRect2:
                cv2.putText(img, 'em cima - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_up(20)
        elif x > bwRect1 and x < ewRect1 and y > ehRect2:
                cv2.putText(img, 'embaixo - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_down(20)
        elif x < bwRect1 and y < bhRect2: 
                cv2.putText(img, 'em cima - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_up(20)
                tello.rotate_counter_clockwise(15)         
        elif x < bwRect1 and y > ehRect2: 
                cv2.putText(img, 'embaixo - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_up()
                tello.rotate_counter_clockwise(15)
        elif x > ewRect1 and y < bhRect2: 
                cv2.putText(img, 'em cima - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_up(20)
                tello.rotate_clockwise(15)            
        elif x > ewRect1 and y > ehRect2: 
                cv2.putText(img, 'embaixo - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2)
                tello.move_down(20)
                tello.rotate_clockwise(15)
                

        
        # Centro de massa da bolinha
        cv2.rectangle(img, (int(x),int(y)), (int(x),int(y)), (0,255,255),3)
        
        # Vetor de direção em relação ao centro da imagem
        cv2.arrowedLine(img, (int(width/2),int(height/2)), (int(x),int(y)), (255,0,0), 2)
    
    return img

def main():
 # Inicia o stream de vídeo
 tello.streamon()
 time.sleep(2)
 
 tello.takeoff()
 frame_read = tello.get_frame_read()
 
 while True:
     tello.send_rc_control(0,0,0,0)
 
     (r,g,b) = cv2.split(frame_read.frame)
     img = cv2.merge([b,g,r])
     # width, height, _ = img.shape
     resized_img = cv2.resize(img, (480, 369))     
     img = idYolo(resized_img, 369, 480)
     
     # img = cv2.resize(img,(640,480))
                 
             
     cv2.imshow("drone", img)
     if cv2.waitKey(1) & 0xff == 27:  # ESC
         break
     
 cv2.destroyAllWindows()
 tello.streamoff()
 tello.land()

if __name__ == "__main__":
 main()
