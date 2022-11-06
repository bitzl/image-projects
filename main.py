from pathlib import Path
import typer
from image_project.html import generate_css_and_js, generate_html, publish

from image_project.image_processing import generate_jp2
from image_project.manifests import generate_manifests

app = typer.Typer()

@app.command()
def main(image_sources: Path, target_path: Path):
    www_path = target_path / "www"
    image_targets = target_path / "images"
    temp_path = Path("temp/")
    typer.echo(f"Read image folders from: {image_sources}")
    typer.echo(f"Generate HTML to: {www_path}")
    typer.echo(f"Generate images and manifests to: {image_targets}")
    typer.echo(f"Temporary files: {temp_path}")
    reset_directory(temp_path)
    generate_jp2(image_sources, www_path)
    generate_manifests(image_targets)
    generate_html(image_targets, temp_path)
    generate_css_and_js(temp_path)
    publish(www_path, temp_path)

def reset_directory(path: Path):
    if path.exists():
        path.rmtree()
    path.mkdir()

if __name__ == "__main__":
    app()