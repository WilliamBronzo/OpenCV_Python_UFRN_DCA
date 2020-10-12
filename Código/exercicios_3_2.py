# import numpy as np
import cv2 as cv


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


def colorir_lista_fun(img, lista_pos, fun):
    fill_list = lista_pos
    img_ret = img.copy()

    num = 0
    for p in fill_list:
        num += 1
        cv.floodFill(img_ret, None, p, fun(num))

    return img_ret


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


def main():

    img = cv.imread('super_bolhas.png', cv.IMREAD_GRAYSCALE)
    if img.data:
        cv.imshow('Bolhas', img)
    else:
        print('Sem imagem!')
        exit(-1)

    saida = labeling_pos(img)

    print('Exercicio 3.2 A:')
    print(f'\nNumero de bolhas: {len(saida)}\nPosições:\n{saida}')

    img2 = colorir_lista_fun(img, saida, lambda x: x % 255)
    cv.imshow('Exercicio 3.2 A (Saida Visual)', img2)

    img3, bolha, bolha_de_bolha = labeling_pos_ref(img)

    print('\n\nExercicio 3.2 B:')
    print(f'\nNumero de bolhas: {len(bolha)}\nPosições:\n{bolha}')
    print(f'\nNumero de bolhas de bolha: {len(bolha_de_bolha)}\nPosições:\n{bolha_de_bolha}')

    cv.imshow('Exercicio 3.2 B', img3)

    cv.waitKey()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
