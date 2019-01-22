# /usr/bin/env python3

from pathlib import Path
import random
import shutil


def process_dir(input_dir, output_dir, percent = 0.7):
    ip = Path(input_dir)
    op = Path(output_dir)

    print("Deleting " + op.as_posix())
    shutil.rmtree(op.as_posix(), ignore_errors=True)

    for category in ip.iterdir():
        output_path = (op / 'train' / category.name).mkdir(parents=True, exist_ok=True)
        output_path = (op / 'validation' / category.name).mkdir(parents=True, exist_ok=True)

    for category in ip.iterdir():
        print("Copying category: {}".format(category.as_posix()).ljust(50), end='')
        train_imgs = 0
        validation_imgs = 0
        for img in category.iterdir():
            if random.random() < percent:
                output_img = op / 'train' / category.name / img.name
                train_imgs += 1
            else:
                output_img = op / 'validation' / category.name / img.name
                validation_imgs += 1

            shutil.copy(img.as_posix(), output_img.as_posix())
        print("=> train({}), validation({})".format(train_imgs, validation_imgs))

if __name__ == '__main__':
    process_dir('imgs/processed', 'imgs/splitted')
