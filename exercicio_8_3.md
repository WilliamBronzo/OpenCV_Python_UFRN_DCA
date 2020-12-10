# Exercício 8.3:
 - Utilizando os programas exemplos/canny.cpp e exemplos/pontilhismo.cpp como referência, implemente um programa cannypoints.cpp. A idéia é usar as bordas produzidas pelo algoritmo de Canny para melhorar a qualidade da imagem pontilhista gerada. A forma como a informação de borda será usada é livre. Entretanto, são apresentadas algumas sugestões de técnicas que poderiam ser utilizadas:  
   - Desenhar pontos grandes na imagem pontilhista básica.
   - Usar a posição dos pixels de borda encontrados pelo algoritmo de Canny para desenhar pontos nos respectivos locais na imagem gerada.
   - Experimente ir aumentando os limiares do algoritmo de Canny e, para cada novo par de limiares, desenhar círculos cada vez menores nas posições encontradas. A Figura 19 foi desenvolvida usando essa técnica.
 - Escolha uma imagem de seu gosto e aplique a técnica que você desenvolveu.
 - Descreva no seu relatório detalhes do procedimento usado para criar sua técnica pontilhista.  
 
# Solução:  
A idéia de fazer o pontilhista é deixa a imagem como se fosse uma pintura feita a mão com apenas toques de pincel circular. Para isso é feita a função:
```Python
def ponto_img(img):
    tamanho = img.shape
    retorno = np.zeros(tamanho, dtype=np.uint8)

    STEP = 4
    JITTER = 3
    RAIO = 4

    xrange = np.arange(0, tamanho[0]-STEP, STEP) + STEP // 2
    yrange = np.arange(0, tamanho[1]-STEP, STEP) + STEP // 2

    np.random.shuffle(xrange)
    for i in xrange:
        np.random.shuffle(yrange)
        for j in yrange:
            x = i + np.random.randint((2 * JITTER) - JITTER + 1)
            y = j + np.random.randint((2 * JITTER) - JITTER + 1)
            cor = img[x, y]
            retorno = cv.circle(retorno, (y, x), RAIO, (int(cor[0]), int(cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)

    return retorno
```
Basicamente, a função dividi a imagem e regiões em quadrados de tamanho `STEP` e para cada esquina de quadrado desloca aleatoriamente em x e y em `JITTER` de forma reta, diferentemente de um deslocamento de um raio e angulo aleatorios, mas quase equivalente. Com esse pixel se pega a cor e o centro do raio e desenha um circulo com a mesma cor e com borda mais suave `cv.LINE_AA` cujo o raio é `RAIO`. Como o algoritimo foi feito pelo professor fiz uma "tradução" para Python e deixei como esta.  

Como o objetivo do exercício é fazer o desenho das borda com o uso da ferramenta Canny com a mesma tecnica então foi feita uma outra função similar:
```Python
def bordar_random(img, fundo, fator=20):
    retorno = fundo.copy()

    for i in range(6, 0, -1):
        pontos = cv.Canny(img, i*fator, i*fator*3)
        pontos = np.where(pontos != 0)
        cordenadas = zip(pontos[0], pontos[1])

        for p in cordenadas:
            cor = img[p]
            retorno = cv.circle(retorno, (p[1], p[0]), i,  (int(cor[0]), int(cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)

    return retorno
```
O intuito da função erá pegar os pixels da bordas de forma aleatoria e desenhar um circulo e "Apagar os vizinho" para não desenhar outro circulo na posição similar, por isso o `bordar_random` como não entendo o "conceito de arte pontilhismo" então foi adquirido TODOS os pontos do Canny com fatores diferentes decresentes `for i in range(6, 0, -1)` (Basicamente 6 ate 1 multiplicado por `fator` defaut: 20):  
```Python
pontos = cv.Canny(img, i*fator, i*fator*3)
pontos = np.where(pontos != 0)
cordenadas = zip(pontos[0], pontos[1])
```  
E apliquei a mesma tecnica de gerar o circulo só que com raio de 6 a 1:
```Python
retorno = cv.circle(retorno, (p[1], p[0]), i,  (int(cor[0]), int(cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)
```
O `retorno` é uma copia de `fundo.copy()`, o que será passado o `ponto_img` para que a imagem fique com efeito de pintura.  
Então:
```Python
def main():
    print("https://pixabay.com/pt/photos/gato-ressaca-vermelho-bonito-1044750/")
    # img = cv.imread('cat.jpg', cv.IMREAD_GRAYSCALE)
    img = cv.imread('cat.jpg')
    img = cv.resize(img, (800, 532))
    if img.data:
        cv.imshow('lena.jpg', img)
    else:
        print('Sem imagem!')

    cv.imshow('Pontos', ponto_img(img))
    retorno = bordar_random(img, ponto_img(img))
    cv.imshow('Saida', retorno)

    cv.waitKey()
```  
Basta aplicar `bordar_random(img, ponto_img(img))` para que o resultado da imagem seja o desejado.

