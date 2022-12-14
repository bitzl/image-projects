from pathlib import Path
import shutil
import subprocess
import typer
from image_project.html import generate_css_and_js, generate_html

from image_project.image_processing import generate_jp2
from image_project.manifests import generate_manifests

app = typer.Typer()

@app.command()
def main(image_sources: Path, temp_path: Path = typer.Option("temp/"), base_url: str  = typer.Option("http://lab.bitzl.io")):
    www_path = temp_path / "www"
    image_targets = temp_path / "images"
    typer.echo(f"Read image folders from: {image_sources}")
    typer.echo(f"Generate HTML to: {www_path}")
    typer.echo(f"Generate images and manifests to: {image_targets}")
    # reset_directory(temp_path)
    generate_jp2(image_sources, temp_path / "images")
    generate_manifests(temp_path / "images", base_url)
    generate_html(temp_path / "images", temp_path / "www")
    generate_css_and_js(temp_path / "www")
    subprocess.call(["rsync", "-aP", temp_path / "images", "root@lab.bitzl.io:/srv/"])
    subprocess.call(["rsync", "-aP", temp_path / "www", "root@lab.bitzl.io:/srv/"])

def reset_directory(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir()

if __name__ == "__main__":
    app()