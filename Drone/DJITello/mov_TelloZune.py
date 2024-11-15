from tello_zune import TelloZune
import numpy as np
import cv2
import time

# Inicializa o objeto TelloZune
tello = TelloZune()

# Inicia a comunicação com o drone Tello
tello.start_tello()

try:
    print("Enviando comando de inicialização...")
    # Envia um comando mínimo de movimento para ativar o modo de comando
    response = tello.send_rc_control(0, 0, 0, 0)  # Define velocidade zero em todas as direções
    time.sleep(3)
    print("Modo de comando ativado com sucesso.")

    # Exemplo de comando de controle
    print("Movendo o drone para frente...")
    tello.send_rc_control(20, 0, 0, 0)  # Move o drone 20cm/s para frente
    time.sleep(2)
    
    print("Movendo o drone para trás")
    tello.send_rc_control(-20, 0, 0, 0) # Movendo 20cm/s para trás
    time.sleep(2)
    
    print("Movendo o drone para direita")
    tello.send_rc_control(0, 20, 0, 0) # Movendo 20cm/s para direita
    time.sleep(2)
    
    print("Movendo o drone para esquerda")
    tello.send_rc_control(0, -20, 0, 0) # Movendo 20cm/s para esquerda
    time.sleep(2)
    
    print("Girando o drone em 15 graus no sentido horário")
    tello.send_rc_control(0, 0, 0, 15) # Girando o drone em 15 graus/s no sentido horário
    time.sleep(2)
    
    print("Girando o drone em 15 graus no sentido anti-horário")
    tello.send_rc_control(0, 0, 0, -15) # Girando o drone em 15 graus/s no sentido anti-horário
    time.sleep(2)
    
    
    #print("Subindo")
    #tello.send_rc_control(0, 0, 20, 0)  # 20 cm/s para cima
    #time.sleep(2)

    #print("Descendo")
    #tello.send_rc_control(0, 0, -20, 0)  # -20 cm/s para baixo
    #time.sleep(2)
    
    

except Exception as e:
    print(f"Erro ao enviar comando: {e}")
finally:
    print("Encerrando conexão com o drone...")
    tello.end_tello()
