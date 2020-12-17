# Exercício 9.2:
 - Utilizando o programa kmeans.cpp como exemplo prepare um programa exemplo onde a execução do código se dê usando o parâmetro nRodadas=1 e inciar os centros de forma aleatória usando o parâmetro KMEANS_RANDOM_CENTERS ao invés de KMEANS_PP_CENTERS.
  - Realize 10 rodadas diferentes do algoritmo e compare as imagens produzidas.
  - Explique porque elas podem diferir tanto.  

# Solução:
Tradução do código do professor na linguagem Python para uma função:
```Python
def prof_kmeans(img):
    nClusters = 8
    nRodadas = 5

    samples = img.copy()
    samples = np.array(samples.reshape(-1, 3))
    samples = samples.astype(np.float32)

    ret, label, center = cv.kmeans(samples,
                                   nClusters,
                                   None,
                                   (cv.TERM_CRITERIA_MAX_ITER | cv.TERM_CRITERIA_EPS, 10000, 0.0001),
                                   nRodadas,
                                   cv.KMEANS_PP_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(img.shape)

    return res2
```
Chamei essa função de `prof_kmeans`.  
No exercício pede a alteração do `nRodadas` para 1 e alterando o `cv.KMEANS_PP_CENTERS` para `cv.KMEANS_RANDOM_CENTERS`, então foi feita outra função com as alterações:
```Python
def meu_kmeans(img):
    nClusters = 8
    nRodadas = 1

    samples = img.copy()
    samples = np.array(samples.reshape(-1, 3))
    samples = samples.astype(np.float32)

    ret, label, center = cv.kmeans(samples,
                                   nClusters,
                                   None,
                                   (cv.TERM_CRITERIA_MAX_ITER | cv.TERM_CRITERIA_EPS, 10000, 0.0001),
                                   nRodadas,
                                   cv.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(img.shape)

    return res2

```
Chamei essa função de `meu_kmeans`.  
Como tambem pede que rode o algoritimo 10 vezes:
```Python
for i in range(11):
        rodada = meu_kmeans(img)
        cv.imshow(f'Rodada {i}', rodada)
```  

Então no `main` fica:
```Python
def main():
    img = cv.imread('lena.jpg', cv.IMREAD_COLOR)
    if img.data:
        # cv.imshow('lena.jpg', img)
        pass
    else:
        print('Sem imagem!')

    original = prof_kmeans(img)
    cv.imshow('Imp original', original)


    for i in range(11):
        rodada = meu_kmeans(img)
        cv.imshow(f'Rodada {i}', rodada)


    cv.waitKey()


if __name__ == '__main__':
    main()
```  

Rodando o programa irá produzir o seguinte resultados:  

![Imagem](https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/Imagens/pycharm64_2020-12-17_16-35-58.png)

O motivo do resultado diferir mas não muinto é porque o algoritimo de K-means é um algoritimo de Clusterização "*Clustering*" e sua convergencia é um local otimo não um global otimo. Por se trata de um algoritimo *NP-hardness* não deterministico. (Ex.: `Rodada 9` e `Rodada 10`)  

Portanto se durante a inicialização do K-means não for bom, ele pode convergir para um local e não para um global otimo, neste caso a alteração do `cv.KMEANS_RANDOM_CENTERS` irá atrapalhar.  

O outro problema que pode atrapalhar a convergencia, e o numero que o K-means irá roda para encontrar a convergencia otima, neste caso o valor de `nRodadas`.  

Por não ser um algoritimo **não** deterministico, ele nem sempre irá dar o mesmo resultado. O que é esperado para um problema de clusterização.

Código:
https://github.com/WilliamBronzo/OpenCV_Python_UFRN_DCA/blob/master/C%C3%B3digo/exercicio_9_2.py
