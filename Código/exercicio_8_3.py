import numpy as np
import cv2 as cv


def ponto_img(img):
    tamanho = img.shape
    retorno = np.zeros(tamanho, dtype=np.uint8)

    STEP = 4
    JITTER = 3
    RAIO = 4

    xrange = np.arange(0, tamanho[0]-STEP, STEP) + STEP // 2
    yrange = np.arange(0, tamanho[1]-STEP, STEP) + STEP // 2

    np.random.shuffle(xrange)
    for i in xrange:
        np.random.shuffle(yrange)
        for j in yrange:
            x = i + np.random.randint((2 * JITTER) - JITTER + 1)
            y = j + np.random.randint((2 * JITTER) - JITTER + 1)
            cor = img[x, y]
            retorno = cv.circle(retorno, (y, x), RAIO, (int(cor[0]), int(cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)

    return retorno


def bordar_random(img, fundo, fator=20):
    retorno = fundo.copy()

    for i in range(6, 0, -1):
        pontos = cv.Canny(img, i*fator, i*fator*3)
        pontos = np.where(pontos != 0)
        cordenadas = zip(pontos[0], pontos[1])

        for p in cordenadas:
            cor = img[p]
            retorno = cv.circle(retorno, (p[1], p[0]), i,  (int(cor[0]), int(cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)

    return retorno


def main():
    print("https://pixabay.com/pt/photos/gato-ressaca-vermelho-bonito-1044750/")
    # img = cv.imread('cat.jpg', cv.IMREAD_GRAYSCALE)
    img = cv.imread('cat.jpg')
    img = cv.resize(img, (800, 532))
    if img.data:
        cv.imshow('lena.jpg', img)
    else:
        print('Sem imagem!')

    cv.imshow('Pontos', ponto_img(img))
    retorno = bordar_random(img, ponto_img(img))
    cv.imshow('Saida', retorno)

    cv.waitKey()


if __name__ == '__main__':
    main()
