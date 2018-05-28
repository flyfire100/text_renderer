import numpy as np
import cv2


class NoiseState(object):
    # 三种横线效果的比例和须为 1
    p = [
        0.25,  # gauss noise
        0.25,  # uniform noise
        0.25,  # sp noise
        0.25  # poisson noise
    ]


# https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv
class Noiser(object):
    def __init__(self):
        self.noisestate = NoiseState()

    def apply(self, img):
        """
        :param img:  word image with big background
        """
        noise_func = np.random.choice([
            self.apply_gauss_noise,
            self.apply_uniform_noise,
            self.apply_sp_noise,
            self.apply_poisson_noise
        ], p=self.noisestate.p)

        return noise_func(img)

    def apply_gauss_noise(self, img):
        """
        Gaussian-distributed additive noise.
        """
        row, col = img.shape

        mean = 0
        stddev = np.sqrt(10)
        gauss_noise = np.zeros((row, col))
        cv2.randn(gauss_noise, mean, stddev)
        out = img + gauss_noise

        return out

    def apply_uniform_noise(self, img):
        """
        Apply zero-mean uniform noise
        """
        row, col = img.shape
        alpha = 0.05
        gauss = np.random.uniform(0 - alpha, alpha, (row, col))
        gauss = gauss.reshape(row, col)
        out = img + img * gauss
        return out

    def apply_sp_noise(self, img):
        """
        Salt and pepper noise. Replaces random pixels with 0 or 255.
        """
        row, col = img.shape
        s_vs_p = 0.5
        amount = np.random.uniform(0.004, 0.01)
        out = np.copy(img)
        # Salt mode
        num_salt = np.ceil(amount * img.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in img.shape]
        out[coords] = 255.

        # Pepper mode
        num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in img.shape]
        out[coords] = 0
        return out

    def apply_poisson_noise(self, img):
        """
        Poisson-distributed noise generated from the data.
        """
        vals = len(np.unique(img))
        vals = 2 ** np.ceil(np.log2(vals))

        if vals < 0:
            return img

        noisy = np.random.poisson(img * vals) / float(vals)
        return noisy
