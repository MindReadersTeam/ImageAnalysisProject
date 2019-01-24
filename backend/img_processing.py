# /usr/bin/env python3

from pathlib import Path
import skimage
from skimage import io
from skimage.filters import sobel
from skimage.filters.rank import mean_bilateral
from skimage.morphology import disk
from skimage.transform import resize

_info = False


def info(msg, end='\n'):
    global _info
    if _info:
        print(msg, end=end)


def set_info(flag):
    global _info
    _info = flag


def load_image(fn, gray=True):
    return skimage.img_as_float64(io.imread(fn, as_gray=gray))


def process_image(img, disk_radius=20):
    return resize(sobel(mean_bilateral(img, disk(disk_radius))), (128, 128), anti_aliasing=True)


def process_and_save_image(img_path, output_path):
    ip = Path(img_path)
    op = Path(output_path)

    img = load_image(ip.as_posix())
    img = process_image(img)
    io.imsave(op.as_posix(), img)


def process_dir(input_dir, output_dir, verbose=False):
    """
    Processes every image in 'input_dir' and results saves in 'output_dir'.
    Processing is executed only on images that not exists in output dir or
    with newer modification time.
    """
    set_info(verbose)
    ip = Path(input_dir)
    op = Path(output_dir)

    for path in ip.iterdir():
        info("Processing: {}".format(path.name), end='')
        output_path = op / path.name
        if output_path.exists() and output_path.stat().st_mtime > path.stat().st_mtime:
            info(" => skip")
            continue

        img = load_image(path.as_posix())
        img = process_image(img)
        io.imsave(output_path.as_posix(), img)
        info(" => done")


if __name__ == "__main__":
    process_dir('data/raw/like', 'data/xd/like')
