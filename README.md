# OpenCV_Python_UFRN_DCA
Repositório contendo a lista e programas de listas do professor Agostinho Brito.

## Exercícios:
- ### Exercício 2.2:
  - a) Esse programa deverá solicitar ao usuário as coordenadas de dois pontos P1 e P2 localizados dentro dos limites do tamanho da imagem e exibir que lhe for fornecida. Entretanto, a região definida pelo retângulo de vértices opostos definidos pelos pontos P1 e P2 será exibida com o negativo da imagem na região correspondente.
  - b) Seu programa deverá trocar os quadrantes em diagonal na imagem.
  
Solução:

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
Explicando:
