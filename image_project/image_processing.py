
from pathlib import Path
import tqdm
import skimage
import glymur

def generate_jp2(src: Path, dest: Path):
    """
    Take alle images from src and generates a new structure as follows:
    dest/name/number.jp2
    """
    dest.mkdir(exist_ok=True, parents=True)
    objects = dict()
    total = sum(1 for _ in src.iterdir())
    for path in tqdm(src.iterdir(), total=total):
        if not path.suffix == ".png":
            continue

        name, iteration = path.stem.split("_")
        base_path = dest / name
        image = skimage.io.imread(path)
        wh = min(image.shape[0], image.shape[1])
        if wh < 32:
            glymur.Jp2k(base_path / f"{iteration}.jp2", data=image, numres=1, tilesize=image.shape[:2], verbose=True)
        elif wh < 512:
            glymur.Jp2k(base_path / f"{iteration}.jp2", data=image, numres=3, tilesize=image.shape[:2], verbose=True)
        if wh < 1024:
            glymur.Jp2k(base_path / f"{iteration}.jp2", data=image, numres=4, tilesize=image.shape[:2], verbose=True)
        else:
            glymur.Jp2k(base_path / f"{iteration}.jp2", data=image, numres=6, tilesize=(1024,1024), verbose=True)
