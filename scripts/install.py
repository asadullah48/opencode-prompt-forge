"""Install only Prompt Forge files; never modify OpenCode permission config."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def install(destination, force=False):
    destination = Path(destination)
    source = ROOT / '.opencode'
    paths = sorted(p.relative_to(source) for p in source.rglob('*') if p.is_file())
    # Preflight the entire batch before the first write.
    for relative in paths:
        target = destination / relative
        if any(parent.is_symlink() for parent in (target, *target.parents)):
            raise ValueError(f'Refusing symlink destination: {target}')
        if target.exists() and not force:
            raise FileExistsError(f'Already exists: {target}. Use --force to replace package files.')
        if target.exists() and not target.is_file():
            raise ValueError(f'Destination is not a file: {target}')
        if any(parent.exists() and not parent.is_dir() for parent in target.parents):
            raise ValueError(f'Destination parent is not a directory: {target}')
    for relative in paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project', type=Path)
    group.add_argument('--global', dest='globally', action='store_true')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    if args.project and not args.project.is_dir():
        parser.error('--project must be an existing directory')
    destination = Path.home() / '.config/opencode' if args.globally else args.project.absolute() / '.opencode'
    print(f'Installing to {destination}')
    try:
        paths = install(destination, args.force)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Installation failed: {error}\n')
    print(f'Installed {len(paths)} files. Restart OpenCode and type /forge.')


if __name__ == '__main__':
    main()
