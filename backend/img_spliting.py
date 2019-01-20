# /usr/bin/env python3

from pathlib import Path
import random
import shutil


def process_dir(input_dir, output_dir, percent = 0.7):
    ip = Path(input_dir)
    op = Path(output_dir)

    for category in ip.iterdir():
        output_path = (op / 'train' / category.name).mkdir(parents=True, exist_ok=True)
        output_path = (op / 'validation' / category.name).mkdir(parents=True, exist_ok=True)

    for category in ip.iterdir():
        for img in category.iterdir():
            if random.random() < percent:
                output_img = op / 'train' / category.name / img.name
            else:
                output_img = op / 'validation' / category.name / img.name

            shutil.copy(img.as_posix(), output_img.as_posix())
