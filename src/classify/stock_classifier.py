import random

import imagehash

from classify.classifier import Classifier

class StockClassifier(Classifier):
    def __init__(self):
        crops = [
            (0.037, 0.752, 0.042, 0.051),
            (0.078, 0.752, 0.042, 0.051),
            (0.119, 0.752, 0.042, 0.051),
            (0.159, 0.752, 0.042, 0.051),
            (0.275, 0.752, 0.042, 0.051),
            (0.315, 0.752, 0.042, 0.051),
            (0.355, 0.752, 0.042, 0.051),
            (0.396, 0.752, 0.042, 0.051),
            (0.511, 0.752, 0.042, 0.051),
            (0.551, 0.752, 0.042, 0.051),
            (0.592, 0.752, 0.042, 0.051),
            (0.633, 0.752, 0.042, 0.051),
            (0.748, 0.752, 0.042, 0.051),
            (0.790, 0.752, 0.042, 0.051),
            (0.829, 0.752, 0.042, 0.051),
            (0.870, 0.752, 0.042, 0.051)
        ]
        super().__init__('head', (24, 24), crops)

    def process(self, img, port):
        n_stocks = 0
        character = 'null'
        for i, crop in enumerate(self.crops[port*4:(port+1)*4]):
            stock_img = img.crop(crop.to_tuple(img.width, img.height))
            (name, similarity) = self.guess_value(stock_img)[0]
            self.save(stock_img, name, f'{similarity:03d}-p{port}-d{i}-{random.randint(1, 65536):04x}')
            # if similarity > 17:
            #     name = None
            #     break
            n_stocks += 1
            character = name
        return (character, n_stocks)
