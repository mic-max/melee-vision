import random

from classify.classifier import Classifier

class DamageClassifier(Classifier):
    def __init__(self):
        crops = [
            (0.140, 0.844, 0.061, 0.082),
            (0.377, 0.844, 0.061, 0.082),
            (0.614, 0.844, 0.061, 0.082),
            (0.852, 0.844, 0.061, 0.082)
        ]
        super().__init__('damage', (32, 36), crops)

    def process(self, img, port):
        # Note: No spaces should come after a digit & No zeros should come before the first non-zero digit
        digits = []
        crop = self.crops[port]
        for i in range(3):
            digit_img = img.crop(crop.to_tuple(img.width, img.height))
            (name, similarity) = self.guess_value(digit_img)[0]
            self.save(digit_img, name, f'{similarity:03d}-p{port}-d{i}-{random.randint(1, 65536):04x}')
            digits.insert(0, name)

            x_delta = 0.035 if name == '1' else 0.054
            crop.x1 -= x_delta
            crop.x2 -= x_delta
        return Classifier.digits_to_num(digits)
