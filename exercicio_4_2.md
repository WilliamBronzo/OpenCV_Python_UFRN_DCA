# Exercício 4.2:
 - a) Utilizando o programa exemplos/histogram.cpp como referência, implemente um programa equalize.cpp. Este deverá, para cada imagem capturada, realizar a equalização do histogram antes de exibir a imagem. Teste sua implementação apontando a câmera para ambientes com iluminações variadas e observando o efeito gerado. Assuma que as imagens processadas serão em tons de cinza.
 - b) Utilizando o programa exemplos/histogram.cpp como referência, implemente um programa motiondetector.cpp. Este deverá continuamente calcular o histograma da imagem (apenas uma componente de cor é suficiente) e compará-lo com o último histograma calculado. Quando a diferença entre estes ultrapassar um limiar pré-estabelecido, ative um alarme. Utilize uma função de comparação que julgar conveniente.
# Solução:  
Um video é um conjunto de imagem sequencial, então fazer uma função geradora de histograma para uma imagem e usar a mesma função para um video se tem o mesmo resultado, só que o histogram ficará animado igual a video. O maior cuidado que se deve ter para video é o acumulo de imagens na memoria.  
O histograma é a soma do numero de observações a cada intervalo de classe. No caso de uma imagem, e a soma do numero da cor de um tipo ou intervalo de de cores de uma imagem para cada tipo ou classe de cor.  
Exemplo:  
Uma imagem **Preto ou Branco** (0 ou 1) o histograma vai ter apenas dois valores (um vetor de tamanho 2), contendo numero de pixel preto (0) na imagem e outro valor contendo numero de pixel branco (1) na imagem. Quando se usa as cores (Cinza, RGB, RGBA, HSV, HSL, HSLA) o calculo do histograma fica maior e com mais dimensões (2D, 3D, 4D).  

A função geradora de grafico de histograma cinza:
```Python
def gerar_img_histograma(img, tamanho):
    hist_altura = tamanho[1]
    hist_largura = tamanho[0]

    hist_data = cv.calcHist([img], [0], None, [hist_largura], [0, 256], accumulate=True)
    cv.normalize(hist_data, hist_data, beta=hist_altura, norm_type=cv.NORM_MINMAX)

    grafico_hist = np.zeros((hist_altura, hist_largura), dtype=np.uint8)

    for i in range(hist_largura):
        cv.line(grafico_hist,
                (i, hist_altura),
                (i, hist_altura - hist_data[i]),
                [256])

    return grafico_hist
```
O objetivo desta função é gerar um grafico do histograma de uma imagem em escala cinza (0 - 255), fazemos o uso da ferramenta `cv.calcHist(...)` para gerar dados do histograma e normalizar com a ferramenta `cv.normalize(...)`, com o loop cria linhas verticais na imagem com os valores do histograma normalizados.  
Resultado desta função tamanho (256, 100):
![Imagem 1](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-13_19-12-56.png)
Resultado desta função tamanho (1024, 500):
![Imagem 2](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-13_19-16-49.png)

Com o uso da função anterior, da para gerar uma imagem do seu histogram para cada componente da cor (RGB) e combina em um unica imagem.
```Python
def gerar_img_histograma_colorido(img, tamanho):
    bgr_planos = cv.split(img)

    grafico_hist_b = gerar_img_histograma(bgr_planos[0], tamanho)
    grafico_hist_g = gerar_img_histograma(bgr_planos[1], tamanho)
    grafico_hist_r = gerar_img_histograma(bgr_planos[2], tamanho)

    grafico_hist_cor = cv.merge([grafico_hist_b, grafico_hist_g, grafico_hist_r])

    return grafico_hist_cor
```
O `cv.merge(...)` faz com que cada imagem com apenas um coponente de cor (Unico canal), se cobine para formar uma imagem colorida de um histograma.

Uma função alternativa:
```Python
def gerar_img_histograma_colorido_sequecial(img, tamanho):
    bgr_planos = cv.split(img)

    hist_altura = tamanho[1]
    hist_largura = tamanho[0]

    grafico_hist_b = gerar_img_histograma(bgr_planos[0], tamanho)
    grafico_hist_g = gerar_img_histograma(bgr_planos[1], tamanho)
    grafico_hist_r = gerar_img_histograma(bgr_planos[2], tamanho)

    grafico_hist_cor = np.zeros((hist_altura * 3, hist_largura, 3), dtype=np.uint8)

    grafico_hist_cor[:hist_altura, :, 2] = grafico_hist_r
    grafico_hist_cor[hist_altura:hist_altura * 2, :, 1] = grafico_hist_g
    grafico_hist_cor[hist_altura * 2:hist_altura * 3, :, 0] = grafico_hist_b

    return grafico_hist_cor
```
Gera uma image coloria separada do histograma da image de entrada.

Exemplo:  
![Imagem 3](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-10-13_19-21-48.png)  
Janelas:  
"Histogram 1": exemplo da função `gerar_img_histograma_colorido_sequecial(img, (256, 100))`.  
"Histogram 2": exemplo da função `gerar_img_histograma_colorido(img, (256, 100))`.(O que vai ser usado.)  
"lena.png COR": imagem de entrada.  

Função decididora cujo objetivo é fazer histograma independentemente do tipo de imagem (Cinza ou RGB).
```Python
def gerar_img_histograma_any(img, tamanho):
    if len(img.shape) == 3:
        return gerar_img_histograma_colorido(img, tamanho)
    if len(img.shape) == 2:
        return gerar_img_histograma(img, tamanho)
```



Criando a função alarme:
```Python
# Variavel global:
anterior = None


def alarme_histogram(img):
    global anterior

    if len(img.shape) == 3:
        bgr_planos = cv.split(img)
        hist_data_b = cv.calcHist(bgr_planos[0], [0], None, [256], [0, 256], accumulate=True)
        hist_data_g = cv.calcHist(bgr_planos[1], [0], None, [256], [0, 256], accumulate=True)
        hist_data_r = cv.calcHist(bgr_planos[2], [0], None, [256], [0, 256], accumulate=True)

        if anterior is None:
            anterior = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
            atual = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
        else:
            atual = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]

        valor_b = np.sum(np.abs(atual[0] - anterior[0]))
        valor_g = np.sum(np.abs(atual[1] - anterior[1]))
        valor_r = np.sum(np.abs(atual[2] - anterior[2]))

        valor = (valor_r + valor_g + valor_b)

        if valor > 1500:
            print(f'Alarme de histograma!     valor = {valor} > 1500')
            anterior = atual

    if len(img.shape) == 2:
        hist_data = cv.calcHist([img], [0], None, [256], [0, 256], accumulate=True)

        if anterior is None:
            anterior = [hist_data[:, 0]]
            atual = [hist_data[:, 0]]
        else:
            atual = [hist_data[:, 0]]

        valor = np.sum(np.abs(atual[0] - anterior[0]))//3

        if valor > 15000:
            print(f'Alarme de histograma!     valor = {valor} > 15000')
            anterior = atual
```

É uma reescrita da combinação de outras funções, `gerar_img_histograma_any(...)`, `gerar_img_histograma_colorido(...)`, `gerar_img_histograma_colorido_sequecial(...)`. Utiliza variavel global `anterior = None`, para guardar o dados do histograma anterior.  

```Python
if anterior is None:
    anterior = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
    atual = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
else:
    atual = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
```
ou
```Python
if anterior is None:
    anterior = [hist_data[:, 0]]
    atual = [hist_data[:, 0]]
else:
    atual = [hist_data[:, 0]]
```
Condição da primeira imagem.  

```Python
valor_b = np.sum(np.abs(atual[0] - anterior[0]))
valor_g = np.sum(np.abs(atual[1] - anterior[1]))
valor_r = np.sum(np.abs(atual[2] - anterior[2]))

valor = (valor_r + valor_g + valor_b)
```
ou
```Python
valor = np.sum(np.abs(atual[0] - anterior[0]))//3
```
Calcula a diferença do histograma e soma (divide por 3 errata: deveria ser por 30 pois em escala de cinza os valores do histogramas são altos em relação a de cores), para que se tenha valor significativo da mudança das cores do abiente.  

```Python
if valor > 1500:
    print(f'Alarme de histograma!     valor = {valor} > 1500')
    anterior = atual
```
ou
```Python
if valor > 15000:
    print(f'Alarme de histograma!     valor = {valor} > 15000')
    anterior = atual
```
O ultimo trecho de código onde a função retorna na saida do terminal o sinal de alarme e mostra o valor do sinal.  

Apesar de não ter som ou outra forma de alerta, o criterio do alarme é simplismente detectar (Verdadeiro ou Falso), o que facilmente pode ser atraves de retorno da função `return True` caso contrario `return False`, com o fim de didatica, decidi usar a função `print(f'...')` como saida.

Demonstração em video:  
[Demonstração youtube link](https://www.youtube.com/watch?v=98guReyWq9w&t)

