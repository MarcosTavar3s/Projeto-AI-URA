from ultralytics import YOLO
import numpy as np
import cv2
import os
import torch

# Importação do modelo
model = YOLO('YOLO Treinado/runs/detect/train3/weights/best.pt')

def main():
  cap = cv2.VideoCapture(0)
  
  while True:
      ret, frame = cap.read()
  
      if not ret:
          print('Erro em acessar a câmera')
          break
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  
      width = int(cap.get(3))
      height = int(cap.get(4))
      
          
      result = model(frame)
      img = result[0].plot()
      cv2.rectangle(img, (int(width/2), 0), (int(width/2), height), (0,255,0), 2)    
      cv2.rectangle(img, (0, int(height/2)), (width, int(height/2)), (0,255,0), 2) 
      # cv2.rectangle(img, (int(width/2-100), int(height/2-100)), (int(width/2+100), int(height/2+100)), (255,0,0), 2)
      
      boxesxywh = result[0].boxes.xywh
      # print(result[0].boxes.xywh)
      
      print(result[0].boxes.conf)
  
      if not len(result[0].boxes.xywh):
          print('Bolas não detectadas')
      
      else:
          size = len(result[0].boxes.xywh)
          
          # Confiabilidade da previsão
          conf = result[0].boxes.conf
  
          # Para todas as bolas detectadas, desenha-se o vetor em direção ao centro
          for i in range(size):
              if conf[i] > 0.5:
                  # Posição das bolas (x e y são o centro do objeto, w e h, a largura e altura da bounding box)
                  x, y, w, h = boxesxywh[i]
                  
                  # Calcular o angulo
                  dx = float(x - width/2)
                  dy = float(y - height/2)
                  
                  angulo_rad = np.arctan2(dy,dx)
                  angulo_graus = np.degrees(-angulo_rad)
                  
                  if int(x) > width/2 and int(y) < height/2:
                      cv2.putText(img, '1 quadrante '+str(angulo_graus), (int(x-w/2),int(y+h/2+20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
                  elif int(x) < width/2 and int(y) < height/2:
                      cv2.putText(img, '2 quadrante '+str(angulo_graus), (int(x-w/2),int(y+h/2+20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
                  elif int(x) < width/2 and int(y) > height/2:
                      cv2.putText(img, '3 quadrante '+str(angulo_graus), (int(x-w/2),int(y+h/2+20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))  
                  else: 
                      cv2.putText(img, '4 quadrante '+str(angulo_graus), (int(x-w/2),int(y+h/2+20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
                  
                  # Número da bola na detecção
                  # cv2.putText(img, 'Bola ' + str(i), (int(x-w/2),int(y+h/2+20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
                  
                  # Vetor de direção em relação ao centro da imagem
                  cv2.arrowedLine(img, (int(width/2),int(height/2)), (int(x),int(y)), (255,0,0), 2)
                  
                  # Centro de massa da bolinha
                  cv2.rectangle(img, (int(x),int(y)), (int(x),int(y)), (0,255,255),3)
              
          
      cv2.imshow('Imagem', img)
  
  
  cap.release()
  cv2.waitKey()
  cv2.destroyAllWindows()
  
if __name__ == "__main__":
  main()
