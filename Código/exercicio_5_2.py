import numpy as np
import cv2 as cv


def filtro(id=0):

    media = np.ones((3, 3))/9

    gaussiano = np.array([1, 2, 1,
                          2, 4, 2,
                          1, 2, 1]).reshape((3, 3))/16

    horizontal = np.array([-1, 0, 1,
                           -2, 0, 2,
                           -1, 0, 1]).reshape((3, 3))

    vertical = np.array([-1, -2, -1,
                         0, 0, 0,
                         1, 2, 1]).reshape((3, 3))

    laplaciano = np.array([0, -1, 0,
                           -1, 4, -1,
                           0, -1, 0]).reshape((3, 3))

    boost = np.array([0, -1, 0,
                      -1, 5.2, -1,
                      0, -1, 0]).reshape((3, 3))

    indices = [media, gaussiano, horizontal, vertical, laplaciano, boost]

    return indices[id]


def aplicar_filtro(img, mat):
    img_ret = cv.filter2D(img, -1, mat)

    return img_ret


def main():
    # cap = cv.VideoCapture('Bird.mp4')
    cap = cv.VideoCapture('video.mp4')
    if not cap.isOpened():
        print('Falha ao abrir o video.')
        exit(-1)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('Frame', frame)

            img = aplicar_filtro(frame, filtro(4))
            cv.imshow('Laplaciano', img)

            img2 = aplicar_filtro(frame, filtro(1))
            img2 = aplicar_filtro(img2, filtro(4))
            cv.imshow('Laplaciano do gaussiano', img2)

            key = cv.waitKey(15)
            if key == 27:
                break

        else:
            cap = cv.VideoCapture('video.mp4')
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
