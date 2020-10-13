import numpy as np
import cv2 as cv


def gerar_img_histograma(img, tamanho):
    hist_altura = tamanho[1]
    hist_largura = tamanho[0]

    hist_data = cv.calcHist([img], [0], None, [hist_largura], [0, 256], accumulate=True)
    cv.normalize(hist_data, hist_data, beta=hist_altura, norm_type=cv.NORM_MINMAX)

    grafico_hist = np.zeros((hist_altura, hist_largura), dtype=np.uint8)

    for i in range(hist_largura):
        cv.line(grafico_hist,
                (i, hist_altura),
                (i, hist_altura - hist_data[i]),
                [256])

    return grafico_hist


def gerar_img_histograma_colorido(img, tamanho):
    bgr_planos = cv.split(img)

    grafico_hist_b = gerar_img_histograma(bgr_planos[0], tamanho)
    grafico_hist_g = gerar_img_histograma(bgr_planos[1], tamanho)
    grafico_hist_r = gerar_img_histograma(bgr_planos[2], tamanho)

    grafico_hist_cor = cv.merge([grafico_hist_b, grafico_hist_g, grafico_hist_r])

    return grafico_hist_cor


def gerar_img_histograma_any(img, tamanho):
    if len(img.shape) == 3:
        return gerar_img_histograma_colorido(img, tamanho)
    if len(img.shape) == 2:
        return gerar_img_histograma(img, tamanho)


def gerar_img_histograma_colorido_sequecial(img, tamanho):
    bgr_planos = cv.split(img)

    hist_altura = tamanho[1]
    hist_largura = tamanho[0]

    grafico_hist_b = gerar_img_histograma(bgr_planos[0], tamanho)
    grafico_hist_g = gerar_img_histograma(bgr_planos[1], tamanho)
    grafico_hist_r = gerar_img_histograma(bgr_planos[2], tamanho)

    grafico_hist_cor = np.zeros((hist_altura * 3, hist_largura, 3), dtype=np.uint8)

    grafico_hist_cor[:hist_altura, :, 2] = grafico_hist_r
    grafico_hist_cor[hist_altura:hist_altura * 2, :, 1] = grafico_hist_g
    grafico_hist_cor[hist_altura * 2:hist_altura * 3, :, 0] = grafico_hist_b

    return grafico_hist_cor


# Variavel global:
anterior = None


def alarme_histogram(img):
    global anterior

    if len(img.shape) == 3:
        bgr_planos = cv.split(img)
        hist_data_b = cv.calcHist(bgr_planos[0], [0], None, [256], [0, 256], accumulate=True)
        hist_data_g = cv.calcHist(bgr_planos[1], [0], None, [256], [0, 256], accumulate=True)
        hist_data_r = cv.calcHist(bgr_planos[2], [0], None, [256], [0, 256], accumulate=True)

        if anterior is None:
            anterior = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
            atual = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]
        else:
            atual = [hist_data_b[:, 0], hist_data_g[:, 0], hist_data_r[:, 0]]

        valor_b = np.sum(np.abs(atual[0] - anterior[0]))
        valor_g = np.sum(np.abs(atual[1] - anterior[1]))
        valor_r = np.sum(np.abs(atual[2] - anterior[2]))

        valor = (valor_r + valor_g + valor_b)

        if valor > 1500:
            print(f'Alarme de histograma!     valor = {valor} > 1500')
            anterior = atual

    if len(img.shape) == 2:
        hist_data = cv.calcHist([img], [0], None, [256], [0, 256], accumulate=True)

        if anterior is None:
            anterior = [hist_data[:, 0]]
            atual = [hist_data[:, 0]]
        else:
            atual = [hist_data[:, 0]]

        valor = np.sum(np.abs(atual[0] - anterior[0]))//3

        if valor > 15000:
            print(f'Alarme de histograma!     valor = {valor} > 15000')
            anterior = atual


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

            histograma = gerar_img_histograma_any(frame, (256, 300))
            cv.imshow('Histograma', histograma)

            alarme_histogram(frame)

            key = cv.waitKey(15)
            if key == ord('q'):
                break
        else:
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
