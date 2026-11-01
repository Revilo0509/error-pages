from pathlib import Path

import minify_html
import rcssmin
import sass
import yaml
from jinja2 import Environment, FileSystemLoader

CWD = Path.cwd()
SOURCE = CWD / "src"
DIST = CWD / "dist"
DIST.mkdir(parents=True, exist_ok=True)

env = Environment(loader=FileSystemLoader(SOURCE))

# Load config
with open(CWD / "config.yaml", "r", encoding="utf-8") as stream:
    config = yaml.safe_load(stream)["errors"]

# Compile and output Scss
with open(SOURCE / "styles.scss", "r") as f:
    compiled = sass.compile(string=f.read())
    minified = rcssmin.cssmin(compiled)

# Render and output html
template = env.get_template("template.html")
for c in config:
    render = template.render(
        code=c["code"], title=c["title"], desc=c["desc"], css=minified
    )
    render = minify_html.minify(render, minify_css=True, minify_js=True)

    output_file = DIST / f"{c['code']}.html"

    output_file.write_text(render, encoding="utf-8")
