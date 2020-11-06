import argparse
import json
import os
import random
from datetime import datetime

from PIL import Image
import imageio

from classify.damage_classifier import DamageClassifier
from classify.stock_classifier import StockClassifier
from classify.timer_classifier import TimerClassifier

def main(args):
    damage_classifier = DamageClassifier()
    stock_classifier = StockClassifier()
    timer_classifier = TimerClassifier()

    # Main
    with imageio.get_reader(args.video, 'ffmpeg') as vid:
        meta = vid.get_meta_data()
        fps = int(meta['fps'])
        (vid_w, vid_h) = meta['size']
        frame_start = args.seconds_start * fps
        frame_end = args.seconds_end * fps

        gameplay_crop = (
            int(args.x_start * vid_w),
            int(args.y_start * vid_h),
            int(args.x_end * vid_w) + 1, # plus 1 since 2nd crop values and exclusive
            int(args.y_end * vid_h) + 1
        )

        for frame in range(frame_start, frame_end, args.sampling_interval):
            vid.set_image_index(frame)
            img = Image.fromarray(vid.get_next_data()).crop(gameplay_crop)

            # Processing
            timer = timer_classifier.process(img).strftime('%M:%S %f')[:-4]
            print(timer, end=' | ')
            for i in range(4):
                damage = damage_classifier.process(img, i)
                (char, n_stocks) = stock_classifier.process(img, i)
                print(f'{n_stocks}x {char} {damage}%', end=' | ')
            print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Melee Video Analyzer')
    parser.add_argument('video')
    parser.add_argument('seconds_start', type=int)
    parser.add_argument('seconds_end', type=int)
    parser.add_argument('sampling_interval', type=int)
    parser.add_argument('x_start', type=float)
    parser.add_argument('y_start', type=float)
    parser.add_argument('x_end', type=float)
    parser.add_argument('y_end', type=float)
    args = parser.parse_args()
    main(args)
