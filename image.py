import argparse
import random

from PIL import Image
import imagehash
import imageio

char_hashes = {}
digit_hashes = []
timer_hashes = []

stock_crops = [[], [], [], []]
damage_crops = [[], [], [], []]
timer_crops = []

ICON_SIMILARITY_THRESHOLD = 15
DIGIT_SIMILARITY_THRESHOLD = 12

icon_hashing_func = imagehash.dhash
digit_hashing_func = imagehash.dhash_vertical

def init_data_structures():
    names = [
        'bowser', 'cfalcon', 'dk', 'drmario', 'falco', 'fox', 'ganondorf', 'icies',
        'jigglypuff', 'kirby', 'link', 'luigi', 'mario', 'marth', 'mewtwo', 'gamenwatch',
        'ness', 'peach', 'pichu', 'pikachu', 'roy', 'samus', 'sheik', 'yoshi', 'younglink', 'zelda'
    ]
    img = Image.open('stock_icons.png')
    W = 24
    for (index, name) in enumerate(names):
        sub_img = img.crop((index * W, 0, (index + 1) * W, img.height))
        sub_hash = icon_hashing_func(sub_img)
        char_hashes[name] = sub_hash

    img = Image.open('damage_digits.png')
    W = 26
    for index in range(10):
        sub_img = img.crop((index * W, 0, (index + 1) * W, img.height))
        sub_hash = digit_hashing_func(sub_img)
        digit_hashes.append(sub_hash)

    img = Image.open('timer_digits.png')
    W = 23
    for index in range(10):
        sub_img = img.crop((index * W, 0, (index + 1) * W, img.height))
        sub_hash = digit_hashing_func(sub_img)
        timer_hashes.append(sub_hash)

    for i in range(4):
        for j in range(4):
            stock_crops[i].append(stock_coords(i, j))
    
    for i in range(4):
        for j in range(3):
            damage_crops[i].append(damage_coords(i, j))

    for i in range(6):
        timer_crops.append(timer_coords(i))

def guess_character(stock_img):
    img_hash = icon_hashing_func(stock_img)
    x = {name: img_hash - v for (name, v) in char_hashes.items()}
    sorted_x = sorted(x.items(), key=lambda x: x[1])
    stock_img.save(f'out/chars/{sorted_x[0][0]}/{sorted_x[0][1]:02d}-{random.randint(1, 65536):04x}.png')
    if sorted_x[0][1] > ICON_SIMILARITY_THRESHOLD:
        return (None, sorted_x[0][1])
    return sorted_x[0]

def guess_digit(digit_img):
    img_hash = digit_hashing_func(digit_img)
    x = {index: img_hash - v for (index, v) in enumerate(digit_hashes)}
    sorted_x = sorted(x.items(), key=lambda x: x[1])
    digit_img.save(f'out/digits/{sorted_x[0][0]}/{sorted_x[0][1]:02d}-{random.randint(1, 65536):04x}.png')
    if sorted_x[0][1] > DIGIT_SIMILARITY_THRESHOLD:
        return (0, sorted_x[0][1])
    return sorted_x[0]

def guess_timer_digit(timer_img):
    img_hash = digit_hashing_func(timer_img)
    x = {index: img_hash - v for (index, v) in enumerate(digit_hashes)}
    sorted_x = sorted(x.items(), key=lambda x: x[1])
    # TODO first digit in the minute time must be between [0-5] not [0-9]
    timer_img.save(f'out/timer/{sorted_x[0][0]}/{sorted_x[0][1]:02d}-{random.randint(1, 65536):04x}.png')
    if sorted_x[0][1] > DIGIT_SIMILARITY_THRESHOLD:
        return (0, sorted_x[0][1])
    return sorted_x[0]

def player_stocks(frame, port: int):
    n_stocks = 0
    character = 'null'
    for stock_num in range(4):
        stock_img = frame.crop(stock_crops[port][stock_num])
        (char, similarity) = guess_character(stock_img)
        if char == None:
            break
        n_stocks += 1
        character = char
    return (character, n_stocks)

def player_damage(frame, port: int) -> int:
    damage = 0
    # Not Possible: "1  ", "1 1", "11 ", " 1 ", "001", "011", "000", " 01"
    # No spaces after a digit, no zeros before the first non-zero digit
    for digit_num in range(3):
        damage_img = frame.crop(damage_crops[port][digit_num])
        (digit, similarity) = guess_digit(damage_img)
        damage += digit * 10 ** (2 - digit_num)
    return damage

def timer_remaining(frame) -> str:
    digits = []
    for timer_num in range(6):
        timer_img = frame.crop(timer_crops[timer_num])
        (digit, similarity) = guess_timer_digit(timer_img)
        digits.append(digit)
    return f'{digits[0]}{digits[1]}:{digits[2]}{digits[3]} {digits[4]}{digits[5]}'

def stock_coords(port: int, stock: int):
    (left, top, right, bottom) = (609, 0, 1920, 1080)
    width = right - left
    height = bottom - top
    
    left_padding = 0.037376
    between = 0.07494279
    stock_width = 0.040617
    stock_height = 0.048148
    top_stock = 0.755555
    return (
        left + width * (left_padding + (port * (stock_width * 4 + between)) + stock * stock_width),
        top + height * (top_stock),
        left + width * (left_padding + (port * (stock_width * 4 + between)) + (stock + 1) * stock_width),
        top + height * (top_stock + stock_height)
    )

def timer_coords(digit_num: int):
    (left, top, right, bottom) = (609, 0, 1920, 1080)
    width = right - left
    height = bottom - top
    lefts = [0.381388, 0.425629, 0.490465, 0.534706, 0.588100, 0.621662]
    digit_top    = 0.112962 if digit_num < 4 else 0.125000
    digit_width  = 0.036613 if digit_num < 4 else 0.029748
    digit_height = 0.046296 if digit_num < 4 else 0.036111

    return (
        left + width * (lefts[digit_num]),
        top + height * (digit_top),
        left + width * (lefts[digit_num] + digit_width),
        top + height * (digit_top + digit_height)
    )

def damage_coords(port: int, digit_number: int):
    left_padding = 662
    digit_width = 66
    digit_height = 74
    top_line = 920
    return (
        left_padding + port * 310 + digit_number * 70,
        top_line,
        left_padding + port * 309 + digit_number * 70 + digit_width,
        top_line + digit_height
    )

def main(args):
    init_data_structures()

    vid = imageio.get_reader(args.video, 'ffmpeg')
    fps = int(vid.get_meta_data()['fps'])

    frame_start = args.seconds_start * fps
    frame_end = args.seconds_end * fps

    for frame in range(frame_start, frame_end, fps + 1):
        vid.set_image_index(frame)
        img = Image.fromarray(vid.get_next_data())
        print(f'{timer_remaining(img)} | ', end='')
        for i in range(4):
            (char, n_stocks) = player_stocks(img, i)
            damage = player_damage(img, i)
            print(f'{char[0:5]:5} {damage:3d}% x{n_stocks}', end=' | ')
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Melee Video Analyzer')
    parser.add_argument('video')
    parser.add_argument('seconds_start', type=int)
    parser.add_argument('seconds_end', type=int)
    args = parser.parse_args()
    main(args)
