from pathlib import Path
from tqdm import tqdm
import skimage
import glymur
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def generate_jp2(src: Path, dest: Path):
    """
    Take alle images from src and generates a new structure as follows:
    dest/name/number.jp2
    """
    dest.mkdir(exist_ok=True, parents=True)

    input_images = sorted(list(src.glob("**/*.png")))
    for path in tqdm(input_images):
        if not path.suffix == ".png":
            continue

        name, iteration = path.stem.split("_")
        base_path = dest / name
        image_path = base_path / f"{iteration}.jp2"
        if image_path.exists():
            continue

        base_path.mkdir(exist_ok=True, parents=True)
        image = skimage.io.imread(path)
        wh = min(image.shape[0], image.shape[1])
        if wh < 32:
            numres=1
            tilesize=image.shape[:2]
        elif wh < 512:
            numres=3
            tilesize=image.shape[:2]
        elif wh < 1024:
            numres=4
            tilesize=image.shape[:2]
        else:
            numres=6
            tilesize=(1024, 1024)
        glymur.Jp2k(
            image_path,
            data=image,
            numres=numres,
            tilesize=tilesize,
            verbose=False,
        )