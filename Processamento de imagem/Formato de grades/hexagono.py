import numpy as np
import cv2
import os

# O codigo faz a leitura de uma imagem e salva a imagem com grades de hexagonos regulares
def main():
    # path = input("Coloque o caminho da imagem aqui: ")
    path = "Imagens - Teste/teste_bola.jpg"
    img = cv2.imread(path)
    height, width, _ = img.shape
              
    # definicao do tamanho dos lados do hexagono
    x = 20 # para a primeira linha nao violar a condicao de ser um poligono regular 
    l = x*(2**(1/2)) # pela condicao inicial de ser regular, o lado tera esse comprimento
    
    # cor da grade em bgr
    grade_cor = (0,0,255)
    
    # fecha o poligono
    isClosed = True
    
    for j in range(int(height//l)):
        for i in range(int(width//l)):    
            # coordenada dos pontos para fazer o hexagono (nao alterar)
            pts = np.array([[x*2*i, x + 2*j*(x+l)], [x*2*i, x + l + 2*j*(x+l)], [x + x*2*i, 2*x + l + 2*j*(x+l)], [2*x + x*2*i, x + l + 2*j*(x+l)], [2*x + x*2*i, x + 2*j*(x+l)], [x + x*2*i, 2*j*(x+l)]], dtype=np.int32)
            
            # pts = np.array([[x*2*i, x], [x*2*i, x+l], [x + x*2*i, 2*x+l], [2*x + x*2*i, x+l], [2*x + x*2*i, x], [x + x*2*i, 0]], np.int32)
            pts = pts.reshape((-1, 1, 2))        
            cv2.polylines(img, [pts], isClosed, grade_cor, 2)
            cv2.rectangle(img, (x + x*2*i,  int(2*x + l + 2*j*(x+l))), (x + x*2*i, int(2*(x+l) + 2*j*(x+l)) ), (0, 0, 255), 2)
            
        
    while True:
        cv2.imshow("Imagem com grades hexagonais", img)
        
        if cv2.waitKey(1) & 0xff == 27:
            break
  
    # nome_arquivo = input("Coloque o nome do arquivo: ")
    # nome_arquivo += ".jpg"
    # cv2.imwrite(nome_arquivo, img)
    # print(f"Arquivo {nome_arquivo} foi salvo com sucesso na pasta {os.getcwd()}")
    
    cv2.destroyAllWindows()
    
if __name__=="__main__":
    main()
