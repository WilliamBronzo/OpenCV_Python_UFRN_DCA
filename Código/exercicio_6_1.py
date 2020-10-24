import numpy as np
import cv2 as cv


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


# Obrigatoriedade da funcao! (Desnecessario!)
def faz_nada(*args, **kwargs):
    pass


def main():

    cap = cv.VideoCapture('People.mp4')
    cv.namedWindow('Frame')
    cv.namedWindow('Padrao')

    cv.createTrackbar('x1', 'Padrao', 250, 1000, faz_nada)
    cv.createTrackbar('x2', 'Padrao', 490, 1000, faz_nada)
    cv.createTrackbar('d', 'Padrao', 0, 100, faz_nada)
    cv.createTrackbar('gauss', 'Padrao', 20,  100, faz_nada)

    if not cap.isOpened():
        print('Falha ao abrir o video.')
        exit(-1)

    speed = 3
    descarte_frame = 0
    while True:
        ret, frame = cap.read()
        if ret:
            if descarte_frame == 0:
                x1 = cv.getTrackbarPos('x1', 'Padrao')
                x2 = cv.getTrackbarPos('x2', 'Padrao')
                d = cv.getTrackbarPos('d', 'Padrao')
                gauss = cv.getTrackbarPos('gauss', 'Padrao')

                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                cv.imshow('Frame', frame)

                img = tiltshift(frame, x1, x2, d, gauss)
                cv.imshow('Padrao', img)

                key = cv.waitKey(15)
                if key == 27:
                    break
                descarte_frame += 1
                descarte_frame = descarte_frame % speed
            else:
                descarte_frame += 1
                descarte_frame = descarte_frame % speed

        else:
            cap = cv.VideoCapture('People.mp4')
    cap.release()
    cv.destroyAllWindows()


def menu():
    pass


if __name__ == '__main__':
    print('https://pixabay.com/pt/videos/pessoas-com%C3%A9rcio-loja-ocupado-6387/')
    main()
