
from dataclasses import dataclass
from pathlib import Path
from typing import List
from glymur import Jp2k

@dataclass
class ImageInfo:
    path: Path
    name: str
    width: int
    height: int
    label: str

    @classmethod
    def from_path(cls, path: Path) -> "Item":
        jp2 = Jp2k(path)
        return cls(path, path.stem, jp2.shape[1], jp2.shape[0], path.stem)

@dataclass
class Item:
    name: str
    path: Path
    images: List[ImageInfo]

    @classmethod
    def from_path(cls, path: Path) -> "Item":
        return cls(path.name, path, [])
