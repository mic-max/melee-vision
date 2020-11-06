import os

from PIL import Image
import imagehash
import imageio

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h

    def to_tuple(self, w, h):
        return (w * self.x1, h * self.y1, w * self.x2, h * self.y2)

class Classifier():
    def __init__(self, directory, size, crops):
        self.masks = {}
        self.hashes = {}

        self.res_dir = os.path.join('res', directory)
        self.out_dir = os.path.join('out', directory)
        self.black_img = Image.new('1', size, 0)
        self.crops = [Rectangle(*x) for x in crops]
        
        # Populates the `masks` and `hashes` dicts
        self.generate_masks_and_hashes()

    def hash_func(self, img):
        return imagehash.dhash(img, hash_size=16)

    def generate_masks_and_hashes(self):
        for filename in os.listdir(self.res_dir):
            img = Image.open(f'{self.res_dir}/{filename}').convert('RGBA')
            grey_img = img.convert('L')
            (name, _) = os.path.splitext(filename)
            self.hashes[name] = self.hash_func(img)
            self.masks[name] = grey_img

    def guess_value(self, img, hashes=None):
        # the `hashes` param can be used to limit the possible guesses
        hashes = self.hashes if hashes is None else hashes
        x = {}
        img = img.resize(self.black_img.size)
        for (name, v) in hashes.items():
            masked_img = Image.composite(img, self.black_img, self.masks[name])
            img_hash = self.hash_func(masked_img)
            x[name] = img_hash - v
        return sorted(x.items(), key=lambda x: x[1])

    def save(self, img, directory, filename):
        img.save(os.path.join(self.out_dir, directory, filename + '.png'))

    @staticmethod
    def digits_to_num(digits):
        result = 0
        for i, v in enumerate(digits):
            result += int(v) * 10 ** (len(digits) - 1 - i)
        return result
