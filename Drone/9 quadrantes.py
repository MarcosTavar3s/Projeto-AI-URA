from ultralytics import YOLO
import numpy as np
import cv2
import os
import torch

# Importação do modelo
model = YOLO('YOLO Treinado/runs/detect/train3/weights/best.pt')

def main():
  cap = cv2.VideoCapture(0)
# 'http://192.168.206.219:81/stream'

  while True:
      ret, frame = cap.read()
  
      if not ret:
          print('Erro em acessar a câmera')
          break
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  
      width = int(cap.get(3)) # largura da imagem captada
      height = int(cap.get(4)) # altura da imagem captada
      
      # Variáveis dos retângulos de referência
      bwRect1 = int(0.3*width)
      ewRect1 = int(0.7*width)
      bhRect2 = int(0.3*height)
      ehRect2 = int(0.7*height)
         
      result = model(frame)
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
                  
          if x > bwRect1 and x < ewRect1 and y > bhRect2 and y < ehRect2:
              cv2.putText(img, 'centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x < bwRect1 and y > bhRect2 and y < ehRect2:
              cv2.putText(img, 'esquerda - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x > ewRect1 and y > bhRect2 and y < ehRect2:
              cv2.putText(img, 'direita - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x > bwRect1 and x < ewRect1 and y < bhRect2:
              cv2.putText(img, 'em cima - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x > bwRect1 and x < ewRect1 and y > ehRect2:
              cv2.putText(img, 'embaixo - centro', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x < bwRect1 and y < bhRect2: 
              cv2.putText(img, 'em cima - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x < bwRect1 and y > ehRect2: 
              cv2.putText(img, 'embaixo - esquerda', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x > ewRect1 and y < bhRect2: 
              cv2.putText(img, 'em cima - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          elif x > ewRect1 and y > ehRect2: 
              cv2.putText(img, 'embaixo - direita', (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
          
          # Centro de massa da bolinha
          cv2.rectangle(img, (int(x),int(y)), (int(x),int(y)), (0,255,255),3)
          
          # cv2.putText(img, str(h.item()), (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
          # Vetor de direção em relação ao centro da imagem
          # cv2.arrowedLine(img, (int(width/2),int(height/2)), (int(x),int(y)), (255,0,0), 2)
        
      cv2.imshow('Imagem', img)
    
  cap.release()
  cv2.waitKey()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
