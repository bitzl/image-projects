from pathlib import Path
import shutil
import subprocess
from jinja2 import Environment, PackageLoader, select_autoescape

def generate_html(items_path: Path, target_path: Path):
    env = Environment(
        loader=PackageLoader("generator"),
        autoescape=select_autoescape()
    )

    template = env.get_template("overview.html.j2")
    item_ids = [p.name for p in sorted(items_path.iterdir()) if p.is_dir()]

    # For now create groups by a common prefix, which means the items have been create roughly at the same time.
    groups = []
    last_prefix = None
    for item_id in item_ids:
        if last_prefix is not None and last_prefix == item_id[:3]:
            groups[-1].append(item_id)
        else:
            last_prefix = item_id[:3]
            groups.append([item_id])
    with open(target_path / "index.html", "w") as f:
        f.write(template.render(groups = groups))

    template = env.get_template("item.html.j2")
    for item_id in item_ids:
        item_path = target_path / item_id
        item_path.mkdir(exist_ok=True)
        with (item_path / "index.html" ).open("w") as f:
            f.write(template.render(name=item_id))


def generate_css_and_js(target_path: Path):
    asset_path = Path("assets/")
    asset_path.mkdir(exists_ok=True)
    source_css = asset_path / "source.css"
    shutil.copy("source.css", source_css)
    subprocess.run(["npx", "tailwindcss", "-i", target_path / "source.css", "-o", asset_path / "style.css"])
    source_css.unlink() # Don't need source.css anymore, we now have style.css from Tailwind
    shutil.copy("node_modules/ @fontsource/400.css", asset_path / "400.css")
    shutil.copy("node_modules/tify/dist/tify.js", asset_path / "tify.js")
    shutil.copy("node_modules/tify/dist/tify.css", asset_path / "tify.css")


def publish(temp_path: Path, target_path: Path):
    shutil.copytree(temp_path, target_path, dirs_exist_ok=True)
