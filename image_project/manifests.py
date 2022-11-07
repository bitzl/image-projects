
import json
from pathlib import Path
from typing import List

from tqdm import tqdm

from image_project import ImageInfo

def manifest(identifier, images: List[ImageInfo], base_url: str):
    return {
        "@id": f"{base_url}/{identifier}/manifest",
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "label": identifier,
        "metadata": [
            { "label": "Project", "value": "RealESRGAN Dreams" },
        ],
        "description": "<p>This is a test description.</p><p>It even has mutiple paragraphs.</p>",
        "thumbnail": {
            "@id": f"{base_url}/iiif/2/{identifier}/03/full/full/0/default.jpg",
            "service": {
            "@id": f"{base_url}/iiif/2/{identifier}/manifest.json",
            "@context": "http://iiif.io/api/image/2/context.json",
            "profile": "http://iiif.io/api/image/2/level1.json"
            }
        },
        "sequences": [
            {
            "@id": f"{base_url}/iiif/2/{identifier}/sequence/normal",
            "@type": "sc:Sequence",
            "startCanvas":  f"{base_url}/iiif/2/{identifier}/canvas/01",
            "canvases": [
                {
                "@type": "sc:Canvas",
                "@id": f"{base_url}/iiif/2/{identifier}/canvas/{image.name}",
                "label": image.name,
                "height": image.height,
                "width": image.width,
                "images": [
                    {
                    "@context": "http://iiif.io/api/presentation/2/context.json",
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "@id": f"{base_url}/iiif/2/{identifier}/annotation/{image.name}",
                    "resource": {
                        "@id": f"{base_url}/iiif/2/{identifier}/{image.name}",
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "service": {
                        "@id": f"{base_url}/iiif/2/{identifier}/{image.name}",
                        "@context": "http://iiif.io/api/image/2/context.json",
                        "profile": "http://iiif.io/api/image/2/level1.json"
                        },
                        "height": image.height,
                        "width": image.width
                    },
                    "on": f"{base_url}/iiif/2/{identifier}/canvas/{image.name}"
                    }
                ]
                }
                for image in images
            ]
            }
        ]
    }

def generate_manifests(item_path: Path, base_url: str):
    total = sum(1 for _ in item_path.iterdir())
    for item in tqdm(item_path.iterdir(), total=total):
        if not item.is_dir():
            continue
    
        image_paths = sorted(path for path in item.iterdir() if path.suffix == '.jp2')
        image_infos = [ImageInfo.from_path(path) for path in image_paths]
        doc = manifest(item.name, image_infos, base_url)
        with open(item / "manifest.json", "w") as f:
            json.dump(doc, f)
