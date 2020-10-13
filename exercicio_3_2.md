# Exercício 3.2:
 - a) Observando-se o programa labeling.cpp como exemplo, é possível verificar que caso existam mais de 255 objetos na cena, o processo de rotulação poderá ficar comprometido. Identifique a situação em que isso ocorre e proponha uma solução para este problema.
 - b) Aprimore o algoritmo de contagem apresentado para identificar regiões com ou sem buracos internos que existam na cena. Assuma que objetos com mais de um buraco podem existir. Inclua suporte no seu algoritmo para não contar bolhas que tocam as bordas da imagem. Não se pode presumir, a priori, que elas tenham buracos ou não.
  
# Solução:
Primeiramente a imagem do exemplo não é complexo o suficiente para ter mais que 255 objetos, então foi criado uma imagem atravez do gimp usando os seguintes efeitos em segintes sequecias:  
 - Cria uma imagem 640x480 Com a opção avançada de Espaço de cor em nivel de cinza e Preencher com a Cor de 1° plano (Preto. Garanta isto na ferramenta de cores)
 - Usando filtro: Filtro > Ruído > Atirar... Com as configurações: Aleatorização: 2.00 e Repetir: 1
 - Usando filtro: Desfocar > Desfoque gausiano. Com as configurações: Tamanho X: 5 e Tamanho Y: 5
 - Usando equalização de cores: Cores > Automatico > Equalizar.
 - Usando filtro: Desfocar > Desfoque gausiano. Com as configurações: Tamanho X: 2 e Tamanho Y: 2
 - Usando ajuste de cores com curva: Cores > Curves... Nesta parte vai com a personalidade de cada um. No geral deve fazer uma curva paraboloide poximo dos valores do maximo, até gerar a imagem desejada.
 - Usando o Threshold: Cores > Threshold. Tambem vai com o gosto de cada um.
 - Exporte a imagem. (Sera imagem cinza)  

OBS.: Nas duas ultimas configurações a pessoa deve ter ideia que as imagem deve ser desconexa uma da outra e deve ser bem variado. Tambem tem outras formas de gerar a imagem. E a unica regra, **absoluta**, nesse pequeno tutorial é de gerar a image com tonalidade cinza, ou seja, a primeira instrução. Afinal com as cores em RGB essas cores podem atrapalhar durante o processamento.  

Imagem resultante:

![Imagem super_bolhas.png](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/super_bolhas.png)

Como é observado a imagem acima, existem bastante objetos e provavelmente tem mais que 255 objetos, onde o olho e mentes humanas não coseguem com facilidades contas em curto espaço de tempo.

Refatorar (Refazer o programa), do labeling da questão, a função `labeling_pos(img, pixel_ref=255)` (labeling posição):
```Python
def labeling_pos(img, pixel_ref=255):
    tamanho = img.shape
    imagem_temp = img.copy()

    point_fill = []
    for i in range(tamanho[0]):
        for j in range(tamanho[1]):
            if imagem_temp[i, j] == pixel_ref:
                cv.floodFill(imagem_temp, None, (j, i), 0)
                point_fill.append((j, i))

    return point_fill
```
A cor do pixel de referencia é 255 (Cor branca), então o programa irá encontrar essa cor e preencherar a região com preto `cv.floodFill(imagem_temp, None, (j, i), 0)`. Em seguida irá guardar a posição encontrada `point_fill.append((j, i))` e depois de terminar de varer a imagem, irá retornar a lista de posições dos objetos encontrado `return point_fill`.  

```Python
saida = labeling_pos(img)

print('Exercicio 3.2 A:')
print(f'\nNumero de bolhas: {len(saida)}\nPosições:\n{saida}')

img2 = colorir_lista_fun(img, saida, lambda x: x % 255)
cv.imshow('Exercicio 3.2 A (Saida Visual)', img2)
```
Onde `len(saida)` é o numero de objetos da saida do programa, neste caso é o numero de bolhas.  
Usa a função `colorir_lista_fun(img, lista_pos, fun)`:
```Python
def colorir_lista_fun(img, lista_pos, fun):
    fill_list = lista_pos
    img_ret = img.copy()

    num = 0
    for p in fill_list:
        num += 1
        cv.floodFill(img_ret, None, p, fun(num))

    return img_ret
```
Cujo o objetivo é nada mais que preencher nas posições especificar com seus respectivos indices modulado em uma função.

Segue a imagem da saida:
![Imagem labeling_pos](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-12_18-39-30.png)

Apesar de estar usando preto no preenchimento devido a função usada (`lambda x: x % 255`), onde varia de 0 a 255, pode ser alterada sem problemas, pois o que é usado é os indices para aplicar a coloração e as posições é o retorno da função não a imagem.

Função para remover bordas:
```Python
def remove_bordas(img, pixel_ref=255):
    tamanho = img.shape
    borda = (tamanho[0] - 1, tamanho[1] - 1)
    img_ret = img.copy()

    for i in range(tamanho[0]):
        if img_ret[i, 0] == pixel_ref:
            cv.floodFill(img_ret, None, (0, i), 0)
        if img_ret[i, borda[1]] == pixel_ref:
            cv.floodFill(img_ret, None, (borda[1], i), 0)

    for j in range(tamanho[1]):
        if img_ret[0, j] == pixel_ref:
            cv.floodFill(img_ret, None, (j, 0), 0)
        if img_ret[borda[0], j] == pixel_ref:
            cv.floodFill(img_ret, None, (j, borda[0]), 0)

    return img_ret
```
Esta função vare as bordas e toda vez que encontra um pixel de cor de referencia, pinta de preto, como são 4 bordas, 2 horizontais e 2 verticais, são 4 condições e 2 loops. E esta função retorna a imagem com os objetos nas bordas pintado de preto `return img_ret`.

Aprimorando a função `labeling_pos(img)` para detectar buracos `labeling_pos_ref(img, pixel_ref=255)` (labeling posição refatorado):

```Python
def labeling_pos_ref(img, pixel_ref=255):
    tamanho = img.shape
    imagem_temp = remove_bordas(img)

    cv.floodFill(imagem_temp, None, (0, 0), 32)

    p_bolha = []
    p_bolha_de_bolha = []
    p_anterior = (0, 0)
    for i in range(tamanho[0]):
        for j in range(tamanho[1]):
            if imagem_temp[i, j] == pixel_ref:
                cv.floodFill(imagem_temp, None, (j, i), 64)
                p_bolha.append((j, i))
            if imagem_temp[i, j] == 0:
                cv.floodFill(imagem_temp, None, (j, i), 128)
                cv.floodFill(imagem_temp, None, p_anterior, 128)
                p_bolha_de_bolha.append((j, i))
            p_anterior = (j, i)

    return imagem_temp, p_bolha, p_bolha_de_bolha
```
O fundo pode ser confundido com o buraco das bolhas então a função pinta de cinza 32 `cv.floodFill(imagem_temp, None, (0, 0), 32)`, garantido pela função `remove_bordas(img)`. a imagem terá 3 cores cinzas, 32 o fundo, 255 as bolhas, 0 os buracos das bolhas, então no loop do labeling, terá 2 condições, caso encontre uma bolha e outro caso encontre um buraco:

```Python
if imagem_temp[i, j] == pixel_ref:
    cv.floodFill(imagem_temp, None, (j, i), 64)
    p_bolha.append((j, i))
```
Igual ao `labeling_pos(img)` onde encontra a bolha e pinta de cinza 64

```Python
if imagem_temp[i, j] == 0:
    cv.floodFill(imagem_temp, None, (j, i), 128)
    cv.floodFill(imagem_temp, None, p_anterior, 128)
    p_bolha_de_bolha.append((j, i))
```
Parecido com `labeling_pos(img)` mas a diferença é a checagem `imagem_temp[i, j] == 0` que checa se é preto, e a outra diferença é que se pinta com cinza o buraco e a bolha `cv.floodFill(imagem_temp, None, (j, i), 128)`(buraco) e `cv.floodFill(imagem_temp, None, p_anterior, 128)` (Bolha). Adiciona o buraco como a posição encontrada `p_bolha_de_bolha.append((j, i))` mas como nome diferente.

Para saber se é buraco ou bolha a função deve guardar o pixel anterior do loop `p_anterior = (j, i)`, onde no final do loop se guarda este valor para a proxima interação.

Como a função `labeling_pos_ref(img, pixel_ref=255)` esta retornando `return imagem_temp, p_bolha, p_bolha_de_bolha`, é posivel visualizar com clareza o que bolha sem buraco e bolha com buraco, mas o interese é as posições pois é por ele que se pode saber quais e quantos são.

```Python
img3, bolha, bolha_de_bolha = labeling_pos_ref(img)

print('\n\nExercicio 3.2 B:')
print(f'\nNumero de bolhas: {len(bolha)}\nPosições:\n{bolha}')
print(f'\nNumero de bolhas de bolha: {len(bolha_de_bolha)}\nPosições:\n{bolha_de_bolha}')

cv.imshow('Exercicio 3.2 B', img3)
```
A imagem 3 de retorno `img3` não é a resposta mas a saida do programa `bolha` e `bolha_de_bolha`. Onde é a posição da bolha e a posição do buraco em que pode ser pintada pela função `colorir_lista_fun(img, lista_pos, fun)`, mas a imagem 3 é um bom classificador de bolha e bolhas com bruracos (bolha de bolha).

Imagem da saida:
![Imagem labeling_pos_ref](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-12_19-15-16.png)

Concluindo. Tirando as bolhas que tocam a borda tem exatamente 468 Bolhas, dentre estas, apenas 268 Bolhas tem buracos. Então guardas essas posições para pintar depois aproveita mais a memoria do computador em vez de usar as cores dos pixel em escala de cinza com 1 Bytes (8 bits). 

Caso queira saber quanto itens suporta até o python der problema é so usar:
```
import sys
print(sys.maxsize)
```
e pegar esse valor e dividir pelo tamanho do objeto que vai ser usado para quardar as posições `sys.getsizeof((x,y))` uma tupla.

No meu computador 59652323 itens podem ser armazenados como posições, mas na imagem (1920x1080) pode ter no maximo 2073600 pixels, então não existe problemas a respeito a memoria em relação a imagem. Mas caso use em algum sistema mais limitado isso deve ser levado em consideração.

Codigo Final:  
https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/C%C3%B3digo/exercicios_3_2.py
