import structlog
from pathlib import Path
import shutil

log = structlog.get_logger()


def symlink(src: Path, dst: Path) -> None:
    # done if src is symlink do dst
    if src.is_symlink() and src.readlink() == dst:
        log.info(f"symlink from '{src}' to '{dst}' already done")
        return

    # if src is symlink but not to dst, remove it
    if src.is_symlink() and not src.readlink() == dst:
        log.info(f"{src} symlinks to '{src.readlink()}'; removing symlink")
        src.unlink()

    # if src exist, move to dst
    if src.exists() and not src.is_symlink():
        log.info(f"moving '{src}' to '{dst}'")
        shutil.copytree(src, dst, dirs_exist_ok=True)
        shutil.rmtree(src)

    # chech if symlink can be created in src
    # no error since game might not be installed
    if not src.parent.exists():
        log.info(f"src path '{src.parent}' does not exist; cannot create symlink.")
        return

    # check if target exists
    if not dst.exists():
        log.error(f"dst '{dst}' does not exist; cannot create symlink.")
        raise RuntimeError(f"dst '{dst}' does not exist; cannot create symlink.")

    # create symlink
    log.info(f"creating symlink from '{src}' to '{dst}'")
    src.symlink_to(dst)
