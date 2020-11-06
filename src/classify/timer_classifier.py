from datetime import datetime
import random

from classify.classifier import Classifier

class TimerClassifier(Classifier):
    def __init__(self):
        crops = [
            (0.423, 0.111, 0.042, 0.051),
            (0.487, 0.111, 0.042, 0.051),
            (0.531, 0.111, 0.042, 0.051),
            (0.586, 0.124, 0.032, 0.039),
            (0.619, 0.124, 0.032, 0.039)
        ]
        super().__init__('timer', (24, 24), crops)

    def process(self, img):
        digits = []
        for i, crop in enumerate(self.crops):
            digit_img = img.crop(crop.to_tuple(img.width, img.height))
            hashes = self.hashes if i != 1 else {k:v for k,v in self.hashes.items() if k < '6'}
            guesses = self.guess_value(digit_img, hashes)
            (name, similarity) = guesses[0]
            if i == 0:
                # print(guesses)
                self.save(digit_img, name, f'{similarity:03d}-{i}-{random.randint(1, 65536):04x}')
            digits.append(name)

        mins = int(digits[0])
        secs = Classifier.digits_to_num(digits[1:3])
        hsec = Classifier.digits_to_num(digits[3:5]) * 10000
        return datetime(1, 1, 1, 0, mins, secs, hsec)
