# Exercício 5.2:
 - Utilizando o programa exemplos/filtroespacial.cpp como referência, implemente um programa laplgauss.cpp. O programa deverá acrescentar mais uma funcionalidade ao exemplo fornecido, permitindo que seja calculado o laplaciano do gaussiano das imagens capturadas. Compare o resultado desse filtro com a simples aplicação do filtro laplaciano.
# Solução:  
Usando as matrizez do filtro espacial do exemplo filtroespacial.cpp, foi criado uma função contendo essas matrizes e retorna com base do ID de cada um:
```Python
def filtro(id=0):

    media = np.ones((3, 3))/9

    gaussiano = np.array([1, 2, 1,
                          2, 4, 2,
                          1, 2, 1]).reshape((3, 3))/16

    horizontal = np.array([-1, 0, 1,
                           -2, 0, 2,
                           -1, 0, 1]).reshape((3, 3))

    vertical = np.array([-1, -2, -1,
                         0, 0, 0,
                         1, 2, 1]).reshape((3, 3))

    laplaciano = np.array([0, -1, 0,
                           -1, 4, -1,
                           0, -1, 0]).reshape((3, 3))

    boost = np.array([0, -1, 0,
                      -1, 5.2, -1,
                      0, -1, 0]).reshape((3, 3))

    indices = [media, gaussiano, horizontal, vertical, laplaciano, boost]

    return indices[id]
```
Tabela dos indices:

ID|Nome do filtro
---|---
0|Média (Defaut)
1|Gaussiano
2|Detector de bordas horizontais
3|Detector de bordas verticais
4|Laplaciano
5|Boost (Atenua as bordas)

A aplicação deste filtro é feita pela função aplicadora:  
```Python
def aplicar_filtro(img, mat):
    img_ret = cv.filter2D(img, -1, mat)

    return img_ret
```
O `filter2D(...)` vai aplicar a matriz em cada pixel da image e retornara a outra image com o filtro aplicado. O `-1` é a definição do `ddepth` cujo o objetivo é definir a profundidade da image e seu tipo de dado (uint8, uint16, floar32, float64 ETC). Mais informações:  
https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#ga27c049795ce870216ddfb366086b5a04  
https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#filter_depths  
Como o objetivo do trabalho é apenas aplicar o efeito sem o uso dos valores de forma precisso, não é nessesario converter a imagem para pontos flutuantes `float`.  

O desenvolvimento para video é parecida com [a atividade anterior 4.2](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/exercicio_4_2.md) o codigo a seguir mostra a aplicação do filtro laplaciano e laplaciano do gaussiano em seguida:
```Python
def main():
    # cap = cv.VideoCapture('Bird.mp4')
    cap = cv.VideoCapture('video.mp4')
    if not cap.isOpened():
        print('Falha ao abrir o video.')
        exit(-1)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('Frame', frame)

            img = aplicar_filtro(frame, filtro(4))
            cv.imshow('Laplaciano', img)

            img2 = aplicar_filtro(frame, filtro(1))
            img2 = aplicar_filtro(img2, filtro(4))
            cv.imshow('Laplaciano do gaussiano', img2)

            key = cv.waitKey(15)
            if key == 27:
                break

        else:
            cap = cv.VideoCapture('video.mp4')
    cap.release()
    cv.destroyAllWindows()
```
O trecho de código faz com que o video fique em loop de repetição até o precionamento da tecla ESC.  
No trecho:
```Python
img = aplicar_filtro(frame, filtro(4))
cv.imshow('Laplaciano', img)
```
Aplica apenas laplaciano e mostra o resultado na janela "Laplaciano".  
No trecho:
```Python
img2 = aplicar_filtro(frame, filtro(1))
img2 = aplicar_filtro(img2, filtro(4))
cv.imshow('Laplaciano do gaussiano', img2)
```
Aplica gaussiano e depois o laplaciano como a questão pede.  

Resultado:
![Imagem 1](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-15_15-04-58.png)  
O calculado o laplaciano do gaussiano é mais escuro do que apenas o laplaciano, porem as linha ficam mais espessas.  
  
Codigo final:
https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/C%C3%B3digo/exercicio_5_2.py  

Demonstração video do Youtube:
https://youtu.be/98guReyWq9w
