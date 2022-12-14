#!/usr/bin/env python3

from skimage.metrics import structural_similarity as ssim
import cv2
from argparse import ArgumentParser
import os
import math


parser = ArgumentParser()
parser.add_argument("-s", "--source-dir", dest="source_dir",
                    help="path to source dir", required=True)
parser.add_argument("-d", "--destination-dir",
                    dest="destination_dir",
                    help="path to destination dir", required=True)
parser.add_argument("-t", "--ssim-threshold",
                    dest="ssim_threshold", type=float,
                    help="SSIM threshold", default=0.9)

args = parser.parse_args()

source_dir = args.source_dir
destination_dir = args.destination_dir
ssim_threshold = args.ssim_threshold


def list_files_recursively(dir_path):
  for root, dirs, files in os.walk(dir_path):
    for f in files:
      file_path = os.path.join(root, f)
      yield file_path

matches = []
no_matches = []

for fs in list_files_recursively(args.source_dir):
  src_img = cv2.imread(fs, cv2.IMREAD_GRAYSCALE)
  if src_img is None:
    continue

  src_ratio = src_img.shape[0] / src_img.shape[1]
  src_img_scaled = cv2.resize(src_img, (100, round(100 / src_ratio)))

  target_found = False

  for fd in list_files_recursively(args.destination_dir):
    dst_img = cv2.imread(fd, cv2.IMREAD_GRAYSCALE)
    if dst_img is None:
      continue

    dst_ratio = dst_img.shape[0] / dst_img.shape[1]


    # These can not be equal if one is vertical and another horizontal.
    if math.copysign(1, src_ratio) != math.copysign(1, dst_ratio):
      continue

    # These can not be equal if ratio of their dimensions differ too much.
    if abs(src_ratio - dst_ratio) > 0.01:
      continue

    dst_img_scaled = cv2.resize(dst_img, (100, round(100 / src_ratio)))
    si = ssim(src_img_scaled, dst_img_scaled)

    if si > ssim_threshold:
      matches.append((fs, fd, si))
      target_found = True
      break

  if not target_found:
    no_matches.append(fs)


print('Matches:')
for fs, fd, si in matches:
  print(os.path.basename(fs), '->', os.path.basename(fd), f'({si})')

print()

print('No matches:')
for fs in no_matches:
  print(f'! No destination found for source image {os.path.basename(fs)}')

print()