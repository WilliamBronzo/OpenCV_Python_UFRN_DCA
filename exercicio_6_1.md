# Exercício 5.2:
 - Utilizando o programa exemplos/addweighted.cpp como referência, implemente um programa tiltshift.cpp. Três ajustes deverão ser providos na tela da interface:
   - um ajuste para regular a altura da região central que entrará em foco;
   - um ajuste para regular a força de decaimento da região borrada;
   - um ajuste para regular a posição vertical do centro da região que entrará em foco. Finalizado o programa, a imagem produzida deverá ser salva em arquivo.
 - Utilizando o programa exemplos/addweighted.cpp como referência, implemente um programa tiltshiftvideo.cpp. Tal programa deverá ser capaz de processar um arquivo de vídeo, produzir o efeito de tilt-shift nos quadros presentes e escrever o resultado em outro arquivo de vídeo. A ideia é criar um efeito de miniaturização de cenas. Descarte quadros em uma taxa que julgar conveniente para evidenciar o efeito de stop motion, comum em vídeos desse tipo.
# Solução:  
De acordo com que foi apresentado na atividade 6. O programa tiltshift foi feito em uma função cuja o efeito desejado será aplicado na imagem:
```Python
def tiltshift(img, x1, x2, d, gauss = 2):
    vetor = np.arange(img.shape[0], dtype=np.float32)

    # Tratamento de erro por divisão de 0 (np.tanh tem tratamento de erro! Verifique as funcoes universais do numpy)
    if d == 0:
        vetor = np.sign((np.tanh((vetor - x1) / 1) - np.tanh((vetor - x2) / 1)) - 1)

        # np.clip não funciona para valores negativos.
        vetor[vetor < 0] = 0
        vetor[vetor > 1] = 1
    else:
        vetor = (np.tanh((vetor - x1) / d) - np.tanh((vetor - x2) / d)) / 2

    mascara = np.repeat(vetor, img.shape[1]).reshape(img.shape[:2])

    img2 = cv.GaussianBlur(img, (gauss * 2 + 1, gauss * 2 + 1), 0)
    if len(img.shape) == 3:
        mascara = cv.cvtColor(mascara, cv.COLOR_GRAY2BGR)

    img_ret = cv.convertScaleAbs(img * mascara + img2 * (1 - mascara))

    return img_ret
```  

Onde x1 e x2 é o limite do boramento, d é a força de decaimento da região borrada, gauss é quanto devera ser borrado a imagem. Todos os valores de entrada exeto a imagem (img), são inteiros.  

Primeiramente o programa gera um vetor com valores de 0 a `img.shape[0]` (Altura da imagem).  

A função do exercicio faz uma divisão de `d` (força de decaimento da região borrada), quando for zero apesar de ter tratamento de erro por divisão de zero por uso de funcoes universais do numpy, neste caso quando fazemdos divisão atravez do uso de um vetor com um valor (array 1D / int), o numpy atribui um valor *not a number* (NaN, Não é um numero), com isso o programa não irá para de funcionar, por algum motivo de alomalia da versão atual do Numpy, Python ou o OpenCV o programa de vez em quando o programa causa erro, como se o programa estivesse usando a divisão global do Python (int / int) que não é esse caso, afina a unica exeção que ocorre é quando a imagem tem altura igual a 1. Então à um tratamento de erro condicionado:
```Python
    if d == 0:
        vetor = np.sign((np.tanh((vetor - x1) / 1) - np.tanh((vetor - x2) / 1)) - 1)

        # np.clip não funciona para valores negativos.
        vetor[vetor < 0] = 0
        vetor[vetor > 1] = 1
    else:
        vetor = (np.tanh((vetor - x1) / d) - np.tanh((vetor - x2) / d)) / 2
```  

A função requer uma mascara do tamanho da imagem, então o vetor é "esticado" até a largura da imagem:  
```Python
mascara = np.repeat(vetor, img.shape[1]).reshape(img.shape[:2])
```  

A função cria uma segunda imagem borrada `img2 = cv.GaussianBlur(img, (gauss * 2 + 1, gauss * 2 + 1), 0)`. Como esta função só aceita valores impares, devido a matriz ter que por obrigação um centro, então é aplicado uma função que retorna valores inerentemente impar `x * 2 + 1` independetemente do valor atribuido.  

A função requer uma outra condição, caso a imagem tenha cor, como a aplicação de mascara será feita pelo Numpy, a hipermatriz deve ser corespodente, então a função é capaz de fazer uma matriz "colorida" `mascara = cv.cvtColor(mascara, cv.COLOR_GRAY2BGR)`.  
 E por final a função faz a aplicação de mascara e o retorna:
 ```Python
 img_ret = cv.convertScaleAbs(img * mascara + img2 * (1 - mascara))
 
 return img_ret
 ```
