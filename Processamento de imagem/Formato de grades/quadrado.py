import cv2

# O codigo faz a leitura de uma imagem e salva a imagem com grades quadradas
def main():
  path = input("Coloque o caminho da imagem aqui:")
  
  img = cv2.imread(path)
  
  height, width, _ = img.shape

  # Quantidade de divisoes ( n x n )
  num_de_divisoes = 5
  
  for i in range(1,num_de_divisoes):
      cv2.rectangle(img, ((width//num_de_divisoes)*i, 0), ((width//num_de_divisoes)*i, height), (0,0,255), 2)
      cv2.rectangle(img, (0, (height//num_de_divisoes)*i), (width, (height//num_de_divisoes)*i), (0,0,255), 2)
  
  for i in range(1,num_de_divisoes+1):
      
      for j in range(1,num_de_divisoes+1):        
          cv2.putText(img, str(j)+'.'+str(i), (((j*2)-1)*(width//(num_de_divisoes*2)), ((i*2)-1)*(height//(num_de_divisoes*2))), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 2)
  
  while True:
      cv2.imshow("Imagem", img)
      
      if cv2.waitKey(1) & 0xff == 27:
          break
      
  cv2.destroyAllWindows()

  nome_arquivo = input("Coloque o nome do arquivo")
  nome_arquivo += ".jpg"
  cv2.imwrite(nome_arquivo, img)

if __name__ =="__main__":
  main()
