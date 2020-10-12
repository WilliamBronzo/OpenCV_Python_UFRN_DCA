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

Refatorar (Refazer o programa), do labeling da questão:
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
