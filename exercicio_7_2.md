# Exercício 7.2:
 - Utilizando o programa exemplos/dft.cpp como referência.
   - Implemente o filtro homomórfico para melhorar imagens com iluminação irregular.
   - Crie uma cena mal iluminada e ajuste os parâmetros do filtro homomórfico para corrigir a iluminação da melhor forma possível.
   - Assuma que a imagem fornecida é em tons de cinza.  

# Solução:  

O filtro homomórfico tem sua implementação com base em Transformada Discreta de Fourier (TDF) bidimensional, o resultado não difere do algoritimo de Transformada rápida de Fourier (FFT) só que a ordem de complexidade do algoritimo é O(N^2) mas apenas para tamanho N^2, contudo existe um algoritimo similar a FFT mas alterado para qualquer tamanho entre as ordens N^2, só olha as [referencias do Numpy](https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html#numpy.fft.fft)!, existem implementações de 1D, 2D e ND (N dimensional).  
Então a implementação do DFT da imagem do algoritifo fica:  
```Python
def dft_np(img, vis=False, shift=False):
    complexo = np.fft.fft2(img)
    if shift:
        complexo_img = np.fft.fftshift(complexo)
    else:
        complexo_img = complexo.copy()

    if vis:
        magnitude, fase = visualizador(complexo_img)

        cv.imshow('Magnitude', magnitude)
        cv.imshow('Fase', fase)

    return complexo
```
O retorno por definição é `np.fft.fft2(img)` mas para visualizar o DFT da imagem, o valor de `vis` (visualização) deve ser verdadeiro, para realizar a troca de quadrante do DFT da imagem deve passar o `shift` como verdadeiro. essa função pode ser inteiramente substituida por `np.fft.fft2(img)` sem qualquer problema, inclusive é mais rapido devido a ` complexo_img = complexo.copy()`.  

Para calcular a inversa do DFT da imagem a função implementada:  
```Python
def dft_inv_np(complexo):
    img_comp = np.fft.ifft2(complexo)
    img = np.real(img_comp)
    return img/255
```
Com o retorno em ponto flutuante, em teoria seria 0 a 1, mas como será aplicado um filtro o retorno é imprevisivel e pode passar destes valores.

Como o filtro homomórfico tem sua implementação em um filtro passa alta, logo é feito a função H(u,v) que será aplicada a DFT da imagem por multiplicação:  
```Python
def gerar_filtro(img, x_0, x_min, x_max, c):
    xx, yy = np.mgrid[:img.shape[0], :img.shape[1]]
    circle = np.sqrt((xx - img.shape[0] / 2) ** 2 + (yy - img.shape[1] / 2) ** 2)

    if c == 0:
        c = 10**-10

    return x_min + (np.tanh((circle - x_0)/c) + 1) / 2 * (x_max - x_min)
```
O `x_0` é o ponto de corte do filtro ("Raio"), o `x_min` é o valor mínimo do filtro, o `x_max` é o valor do máximo do filtro e o `c` é a curvatura do filtro (suavização).

Como a inversa da DFT será aplicada, não podera ser garantido os valores dentro do range de 0 a 1 o que pode ser um problema para visualizar esse valores então é feita uma função para normalizar a imagem:  
```Python
def normalizacao(x):
    min_v = np.min(x)
    ran_v = np.max(x) - min_v
    return (x - min_v) / ran_v
```
Basicamente é a formula da normalização na qual irá garantir o valor de 0 a 1, contudo existe uma exeção muito improvavel, quando todos os valores são iguais `ran_v` = 0.  

Posteriormente foi feita uma função apenas para observar a magnitude e a faze do DFT da imagem:
```Python
def visualizador(complexo_img):
    magnitude = np.log(np.abs(complexo_img) + 10**-10)
    magnitude = magnitude / np.max(magnitude)

    fase = (np.angle(complexo_img) + np.pi) / (np.pi * 2)

    return magnitude, fase
```
Como a faze vai de -pi a pi, é normalizado, e a magnitude é sempre positivo != 0, aplicada um log para poder visualizar ou irá ver apenas um ponto.  

A implementação do filtro homomórfico:  
```Python
def filtro_homomorfico(img, x_0, x_min, x_max, c, logs=True):
    if logs:
        img_return = img + 1.
        img_return = np.log(img_return)
    else:
        img_return = img
    img_return = dft_np(img_return)
    filtro = gerar_filtro(img_return, x_0, x_min, x_max, c)
    img_return = img_return * np.fft.fftshift(filtro)
    filtro_return, _ = visualizador(img_return)
    filtro_return = np.fft.fftshift(filtro_return)
    img_return = dft_inv_np(img_return)

    filtro_return[:,:filtro_return.shape[1]//2] = filtro[:,:filtro_return.shape[1]//2]
    return normalizacao(np.exp(img_return)), filtro_return
```
É aplicada antes do DFT da imagem é um log da imagem (de forma opcional não aplicar o log) uma sequencia de algoritimos:
 - Logaritmo da imagem:
```Python
img_return = img + 1.
img_return = np.log(img_return)
```
 - DFT:
```Python
img_return = dft_np(img_return)
```
 - Filtro passa alta:
```Python
filtro = gerar_filtro(img_return, x_0, x_min, x_max, c)
```
 - Troca de quadrante do filtro junto com a multiplicação do DFT da imagem:
```Python
img_return = img_return * np.fft.fftshift(filtro)
```
 - (VISUALIZAÇÂO) Visualizar o DFT da imagem (Descatar a angulo da imagem e adquirir a magnitude):
```Python
filtro_return, _ = visualizador(img_return)
```
 - (VISUALIZAÇÂO) Trocar o quadrante da magnitude do DFT da imagem:
```Python
filtro_return = np.fft.fftshift(filtro_return)
```
 - Calcular a inversa do DFT da imagem com o filtro aplicado:
```Python
img_return = dft_inv_np(img_return)
```
 - (VISUALIZAÇÂO) Fazer um "side by side" do filtro apenas para observar:
```Python
filtro_return[:,:filtro_return.shape[1]//2] = filtro[:,:filtro_return.shape[1]//2]
```
 - Retorne a normalização da exponencial da imagem filtrada (Garantido de 0 a 1) e o filtro para observação:
```Python
return normalizacao(np.exp(img_return)), filtro_return
```
A visualização não faz parte do algoritimo mas serve para observar a parte complexa e ver o filtro aplicado juntos em uma imagem.  

Aplicando a função para um video assim como foi feita para outras atividades:
```Python
def main():
    cv.getBuildInformation()
    # cap = cv.VideoCapture('Bridge.mp4')
    # cap = cv.VideoCapture('Night_Scene.mp4')
    cap = cv.VideoCapture('Highway.mp4')


    if not cap.isOpened():
        print('Falha ao abrir o video.')
        exit(-1)

    cv.namedWindow('Filtro')

    cv.createTrackbar('log', 'Filtro', 1, 1, faz_nada)
    cv.createTrackbar('c', 'Filtro', 10, 100, faz_nada)
    cv.createTrackbar('raio', 'Filtro', 20, 1000, faz_nada)
    cv.createTrackbar('min', 'Filtro', 0, 100, faz_nada)
    cv.createTrackbar('max', 'Filtro', 100, 100, faz_nada)

    speed = 5
    descarte_frame = 0
    while True:
        ret, frame = cap.read()
        if ret:
            if descarte_frame == 0:
                logs = cv.getTrackbarPos('log', 'Filtro')
                c = cv.getTrackbarPos('c', 'Filtro')
                r = cv.getTrackbarPos('raio', 'Filtro')
                v_min = cv.getTrackbarPos('min', 'Filtro')
                v_max = cv.getTrackbarPos('max', 'Filtro')

                v_min = v_min / 100
                v_max = v_max / 100

                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                cv.imshow('Frame', frame)
                img, filtro = filtro_homomorfico(frame, r, v_min, v_max, c, logs==1)
                cv.imshow('Homomorfico', img)
                cv.imshow('Filtro', filtro)

            descarte_frame = (descarte_frame + 1) % speed

            key = cv.waitKey(15)
            if key == 27:
                break
        else:
            # break
            cap = cv.VideoCapture('Highway.mp4')

    cap.release()
    cv.destroyAllWindows()
```
A configuração do filtro é dificil devido a diversos algoritimos, incluindo a normalização, tambem igual dificuldade foi achar um video com uma cena mal iluminado ou com uma iluminação inregular, geralmente são videos noturnas que tem essa caracteristica.
