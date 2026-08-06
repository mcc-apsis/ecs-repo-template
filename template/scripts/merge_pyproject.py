# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "tomli_w",
#     "jinja2",
#     "pyyaml",
# ]
# ///

import tomllib
import tomli_w
import yaml
import jinja2
import subprocess
import re
import keyword
from pathlib import Path

TEMPLATE_FILE = Path("pyproject.toml.jinja.src")


def read_answers():
    """Read copier answers from .copier-answers.yml."""
    with open(".copier-answers.yml") as f:
        return yaml.safe_load(f)


def render_template(answers):
    """Render ._pyproject.toml.jinja with copier answers."""
    template_text = TEMPLATE_FILE.read_text()
    template = jinja2.Template(template_text)
    rendered = template.render(**answers)
    return tomllib.loads(rendered)


def get_old_pyproject():
    """Fetch pyproject.toml from git HEAD (for updates)."""
    try:
        with open("pyproject.toml", "rb") as f:
            return tomllib.load(f)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    
def get_package_name(dep: str) -> str:
    """Extract base package name from dependency string."""
    return dep.split('[')[0].split('>')[0].split('<')[0].split('=')[0].split('!')[0]


def merge_dependencies(new_deps: list[str], old_deps: list[str]) -> list[str]:
    """Merge dependency lists by package name (union)."""
    old_names = {get_package_name(d) for d in old_deps}
    return list(old_deps) + [d for d in new_deps if get_package_name(d) not in old_names]


def merge_configs(new_config: dict, old_config: dict):
    """Merge: take tool config from new, merge dependencies."""
    old_deps: list[str] = old_config.get("project", {}).get("dependencies", [])
    new_deps: list[str] = new_config.get("project", {}).get("dependencies", [])
    
    if old_deps:
        merged = merge_dependencies(new_deps, old_deps)
        new_config["project"]["dependencies"] = merged

    return new_config

def generate_normal_project_name(name: str) -> str:
    """Normalize project name to valid Python package name."""
    # Lowercase and replace spaces/dashes with underscores
    normalized = name.lower().replace('-', '_').replace(' ', '_')
    # Remove any non-alphanumeric and non-underscore characters
    normalized = re.sub(r'[^a-z0-9_]', '', normalized)
    # Collapse multiple underscores
    normalized = re.sub(r'_+', '_', normalized)
    # Remove leading/trailing underscores
    normalized = normalized.strip('_')
    # Ensure doesn't start with digit
    if normalized and normalized[0].isdigit():
        normalized = f'pkg_{normalized}'
    # Avoid Python keywords
    if keyword.iskeyword(normalized):
        normalized = f'{normalized}_pkg'
    return normalized or 'package'

def normalise_name(name: str, config: dict):
    """Normalise project name for package compatibility."""
    normalised_name = generate_normal_project_name(name)
    if 'tool' in config and 'hatch' in config['tool']:
        hatch = config['tool']['hatch']
        if 'build' in hatch and 'targets' in hatch['build']:
            hatch['build']['targets']['wheel']['packages'] = [f"src/{normalised_name}"]

    old_path = Path(f"src/{name}")
    new_path = Path(f"src/{normalised_name}")
    if old_path.exists() and old_path != new_path:
        old_path.rename(new_path)

def main():
    # Read answers and render template
    answers = read_answers()
    new_config = render_template(answers)
    
    # Get old config from git (if update)
    old_config = get_old_pyproject()
    
    # Merge
    if old_config:
        new_config = merge_configs(new_config, old_config)

    normalise_name(answers["projectname"], new_config)
    
    # Write back
    with open("pyproject.toml", "wb") as f:
        tomli_w.dump(new_config, f)
    
    # Clean up
    TEMPLATE_FILE.unlink()
    Path(__file__).unlink()


if __name__ == "__main__":
    main()
