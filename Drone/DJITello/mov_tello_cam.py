from tello_zune import TelloZune
import numpy as np
import cv2
import time

# Inicializa o objeto TelloZune
tello = TelloZune()

# Inicia a comunicação com o drone Tello
tello.start_tello()

# Envia um comando mínimo para ativar o modo de comando
try:
    print("Enviando comando de inicialização...")
    tello.send_rc_control(0, 0, 0, 0)  # Define velocidade zero em todas as direções
    time.sleep(3)
    print("Modo de comando ativado com sucesso.")
    
    print("Girando o drone em 15 graus no sentido anti-horário")
    tello.send_rc_control(0, 0, 0, -15) # Girando o drone em 15 graus/s no sentido anti-horário
    # time.sleep(2)

    # Loop para capturar e exibir o vídeo da câmera do drone
    while True:
        # Captura o frame da câmera
        frame = tello.get_frame()
        
        if frame is not None:
            # Converte o frame para uma imagem OpenCV se necessário
            # frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
            
            # Exibe o frame
            cv2.imshow("Camera do Tello", frame)

            # Sai do loop ao pressionar a tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Não foi possível obter o frame do Tello.")
            break

except Exception as e:
    print(f"Erro ao enviar comando: {e}")

finally:
    # Finaliza a exibição e a conexão com o drone
    cv2.destroyAllWindows()
    print("Encerrando conexão com o drone...")
    tello.end_tello()
