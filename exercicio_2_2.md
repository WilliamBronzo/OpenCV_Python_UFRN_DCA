# Exercício 2.2:
  - a) Esse programa deverá solicitar ao usuário as coordenadas de dois pontos P1 e P2 localizados dentro dos limites do tamanho da imagem e exibir que lhe for fornecida. Entretanto, a região definida pelo retângulo de vértices opostos definidos pelos pontos P1 e P2 será exibida com o negativo da imagem na região correspondente.
  - b) Seu programa deverá trocar os quadrantes em diagonal na imagem.
  
# Solução:

Para inverter as core de uma imagem em escala cinza com profundidade de cor com 8 bits (1 byte) que varia de 0 a 255 (UInt8) deve-se fazer a seguinte formula no pixel em questão: 255-x onde x é o valor deste pixel.

Segue a função:
```Python
def regiao_funcao(img, p1, p2, fun):
    img_ret = img.copy()


    for i in range(min(p1[0], p2[0]), max(p1[0], p2[0])):
        for j in range(min(p1[1], p2[1]), max(p1[1], p2[1])):
            img_ret[i, j] = fun(img[i, j])


    return img_ret
```
Explicando a função:
  
Entrada:  
img --> uma imagem.  
p1 e p2 --> pontos, podendo ser tupla ou lista com tamanho 2 ou maior mas apenas 2 primeiros serão contados.  
fun --> função aplicadora no pixel, ele será responsavel por fazer a alteração no pixel em questão.
  
Com dois loops se vare a região aplicando a função no pixel, essa função é generica.
  
Entrada de imagem:
```Python
file_image = "lena.jpg"
if len(sys.argv) >= 2:
    file_image = sys.argv[1]

img = cv.imread(file_image, cv.IMREAD_GRAYSCALE)
```
  
Entrada de usuario:
```Python
print('Exercicio 2.2 A:\n')
ponto1 = input('Posição do ponto 1 separado por espaços: ')
ponto1 = [int(s) for s in ponto1.split() if s.isdigit()]
ponto1 = ponto1[0:2]

ponto2 = input('Posição do ponto 2 separado por espaços: ')
ponto2 = [int(s) for s in ponto2.split() if s.isdigit()]
ponto2 = ponto2[0:2]
```
O *imput* é a função responsavel por receber a entrada do usuario em string, logo requer tratamento de dados, o tratamento da linha seguinte é feita um *split* da string e para cada elemento condicionado a *isdigit()* sera retornada a *int()* para conversão, isso ira torna valido ou invalido caso os numeros sejam 2 na linha subsequentemente.
  
Em outras palavras é valido:  
"100 200"  
"Ponto 100 e 200"  
"Texto qualquer desde que não tenha numero. Um numero 200 a ate 300 é o ponto A. E outro texto qualque e este pode ter numero mas será ignorado." (Linha unica.)  
  
É invalido:  
"Ponto 100,200"  
"(100,200)"  
"100.200"  
"1,2 3,4"  
"100.0 200.0"  
"100,0 200,0"  
  
A função responsavel por inverter a região é:
```Python
img2 = regiao_funcao(img, ponto1, ponto2, lambda x: 255-x)
```
Com o "lambda x: 255-x" responsavel por inverte o pixel em escala de cinza.
  
  
A segunda parte do problema é a troca de quadrante é um deslocamento de imagem por módulo "%".  
Muito simila a primeira função só que é aplicada a toda a figura.
  
Segue a função:
```Python
def troca_regiao(img, p):
    tamanho = img.shape[:2]
    img_ret = img.copy()

    for i in range(tamanho[0]):
        for j in range(tamanho[1]):
            img_ret[i, j] = img[(i - p[0]) % tamanho[0], (j - p[1]) % tamanho[1]]

    return img_ret
```
Reque uma imagem e o ponto de deslocamento. portanto em cada eixo é aplicada "(x-p.x) % tam.x" onde x é o pixel de referencia do eixo x, p.x é o ponto x do deslocamento, e o tam.x é o tamanho da imagem. Tambem é replicado no eixo y.
  
Aplicação:  
```Python
img3 = troca_regiao(img, ponto1)
```
  
O programa completo:  
https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/51186356a5f259040a5c779d5dc47162f29b6428/C%C3%B3digo/exercicio_2_2.py
  
O uso do programa:
```
python exercicio_2_2.py lena.jpg
```
  
Entradas de usuario:  
100 200  
300 400  
100 300  
  
Imagem da saidas:  
![Imagem do Exercício 2.2](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-01_18-29-38.png)
