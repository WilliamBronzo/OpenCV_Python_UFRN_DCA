import numpy as np
import cv2 as cv


def visualizador(complexo_img):
    magnitude = np.log(np.abs(complexo_img) + 10**-10)
    magnitude = magnitude / np.max(magnitude)

    fase = (np.angle(complexo_img) + np.pi) / (np.pi * 2)

    return magnitude, fase


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


def dft_inv_np(complexo):
    img_comp = np.fft.ifft2(complexo)
    img = np.real(img_comp)
    return img/255


def gerar_filtro(img, x_0, x_min, x_max, c):
    xx, yy = np.mgrid[:img.shape[0], :img.shape[1]]
    circle = np.sqrt((xx - img.shape[0] / 2) ** 2 + (yy - img.shape[1] / 2) ** 2)

    if c == 0:
        c = 10**-10

    return x_min + (np.tanh((circle - x_0)/c) + 1) / 2 * (x_max - x_min)


def normalizacao(x):
    min_v = np.min(x)
    ran_v = np.max(x) - min_v
    return (x - min_v) / ran_v


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


# Obrigatoriedade da funcao! (Desnecessario!)
def faz_nada(*args, **kwargs):
    pass


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


if __name__ == '__main__':
    main()

    # Delete antes de postar:
    # import cProfile
    # cProfile.run('main()', 'output.dat')
