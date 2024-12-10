from pyardrone import ARDrone, at
import time
import cv2

# Inicialize o drone
drone = ARDrone()

drone.navdata_ready.wait()
drone.send(at.CONFIG('general:navdata_demo', True))

# Inicialize o vídeo
drone.video_ready.wait()

while not drone.state.fly_mask:
		drone.takeoff()
time.sleep(2)


# Exibe o nível da bateria
while True:
	img = drone.frame
	battery_level = drone.navdata.demo.vbat_flying_percentage

	cv2.putText(img, 'bateria: ' + str(battery_level), (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0))

	cv2.imshow('img', img)

	# LEMBRAR DE EDITAR ISSO - O DRONE NEM VOA PORQUE A ALTITUDE COMEÇA EM 0
	print(drone.navdata.demo.altitude)
 
	if drone.navdata.demo.altitude == 0:
		break

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
		print('down') 

	if cv2.waitKey(1) & 0xFF == 27:
			break
    
while drone.state.fly_mask:
    drone.land()

cv2.destroyAllWindows()
# Finalize a conexão com o drone
drone.close()
