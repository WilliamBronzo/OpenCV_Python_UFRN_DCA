import numpy as np
import cv2 as cv


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