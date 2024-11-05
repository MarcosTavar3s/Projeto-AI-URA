from pyardrone import ARDrone, at
import time
import cv2

# Inicializa o drone
drone = ARDrone()

# Espera a navdata está pronta
drone.navdata_ready.wait()

# Configuração para acessar o navdata_demo
drone.send(at.CONFIG('general:navdata_demo', True))

# Espera o vídeo está pronto
drone.video_ready.wait()
time.sleep(2)

# Função main
def main():
  # Decolar
  while not drone.state.fly_mask:
  		drone.takeoff()
  
  while True:
  	img = drone.frame
    
    # Nível da bateria
  	battery_level = drone.navdata.demo.vbat_flying_percentage
  	cv2.putText(img, 'bateria: ' + str(battery_level), (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))
  
    # Mostra a imagem
  	cv2.imshow('img', img)
  
  	if cv2.waitKey(1) & 0xFF == ord('w'):
  		drone.move(forward=0.4)
  		print('frente')
  
  	if cv2.waitKey(1) & 0xFF == ord('a'):
  		drone.move(left=0.4)
  		print('esquerda')
  		
  	if cv2.waitKey(1) & 0xFF == ord('d'):
  		drone.move(right=0.4)
  		print('direita')
  		
  	if cv2.waitKey(1) & 0xFF == ord('s'):
  		drone.move(backward=0.4)
  		print('atrás')
  
  	if cv2.waitKey(1) & 0xFF == ord('g'):
  		drone.move(cw=0.4)
  		print('horario')
  
  	if cv2.waitKey(1) & 0xFF == ord('h'):
  		drone.move(ccw=0.4)
  		print('antihorario')
  
  	if cv2.waitKey(1) & 0xFF == ord('u'):
  		drone.move(up=0.4)
  		print('up')
  
  	if cv2.waitKey(1) & 0xFF == ord('j'):
  		drone.move(down=0.4)
  		print('up') 
  
  	if cv2.waitKey(1) & 0xFF == 27:
  			break
  
  # Aterrisar
  while drone.state.fly_mask:
      drone.land()
  
  cv2.destroyAllWindows()
  # Finalize a conexão com o drone
  drone.close()

if __name__ == '__main__':
    main()
