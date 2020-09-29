import sys
import cv2 as cv


def regiao_funcao(img, p1, p2, fun):
    img_ret = img.copy()

    for i in range(min(p1[0], p2[0]), max(p1[0], p2[0])):
        for j in range(min(p1[1], p2[1]), max(p1[1], p2[1])):
            img_ret[i, j] = fun(img[i, j])

    return img_ret


def troca_regiao(img, p):
    tamanho = img.shape[:2]
    img_ret = img.copy()

    for i in range(tamanho[0]):
        for j in range(tamanho[1]):
            img_ret[i, j] = img[(i - p[0]) % tamanho[0], (j - p[1]) % tamanho[1]]

    return img_ret


def main():

    file_image = "lena.jpg"
    if len(sys.argv) >= 2:
        file_image = sys.argv[1]

    img = cv.imread(file_image, cv.IMREAD_GRAYSCALE)

    print('Exercicio 2.2 A:\n')
    ponto1 = input('Posição do ponto 1 separado por espaços: ')
    ponto1 = [int(s) for s in ponto1.split() if s.isdigit()]
    ponto1 = ponto1[0:2]

    ponto2 = input('Posição do ponto 2 separado por espaços: ')
    ponto2 = [int(s) for s in ponto2.split() if s.isdigit()]
    ponto2 = ponto2[0:2]

    print('\n\nExercicio 2.2 B:\n')
    ponto1 = input('Posição do ponto 1 separado por espaços: ')
    ponto1 = [int(s) for s in ponto1.split() if s.isdigit()]
    ponto1 = ponto1[0:2]

    img2 = regiao_funcao(img, ponto1, ponto2, lambda x: 255-x)
    cv.imshow('Exercicio 2.2 A', img2)

    img3 = troca_regiao(img, ponto1)
    cv.imshow('Exercicio 2.2 B', img3)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
