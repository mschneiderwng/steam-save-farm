import tempfile
from pathlib import Path
import ssf.files
import pytest


def test_already_done():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # create what we want to have after we run ssf
        dst.mkdir()
        save_file = dst / "save.txt"
        src.symlink_to(dst)
        save_file.touch()

        assert src.is_symlink() and src.readlink() == dst
        assert (dst / "save.txt").exists()


def test_move_and_symlink():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # standard setup for a new steam game
        src.mkdir()
        save_file = src / "save.txt"
        save_file.touch()

        # run ssf
        ssf.files.symlink(src, dst)

        assert src.is_symlink() and src.readlink() == dst
        assert (dst / "save.txt").exists()


def test_src_symlinks_elsewhere():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # dst exists
        dst.mkdir()
        dst_file = dst / "dst_save.txt"
        dst_file.touch()

        # src is symlink but not to dst
        src.symlink_to("/")

        # run ssf
        ssf.files.symlink(src, dst)

        assert src.is_symlink() and src.readlink() == dst
        assert (dst / "save.txt").exists() is False


def test_dst_already_exists():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # src exists
        src.mkdir()
        save_file = src / "src_save.txt"
        save_file.touch()

        # dst exists
        dst.mkdir()
        dst_file = dst / "dst_save.txt"
        dst_file.touch()

        # run ssf
        ssf.files.symlink(src, dst)

        assert src.is_symlink() and src.readlink() == dst
        assert (dst / "src_save.txt").exists()
        assert (dst / "dst_save.txt").exists()


def test_only_symlink():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # dst exists
        dst.mkdir()
        dst_file = dst / "dst_save.txt"
        dst_file.touch()

        # run ssf
        ssf.files.symlink(src, dst)

        assert src.is_symlink() and src.readlink() == dst
        assert (dst / "save.txt").exists() is False


def test_only_symlink_without_target():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # run ssf
        with pytest.raises(RuntimeError):
            ssf.files.symlink(src, dst)


def test_game_not_installed():
    with tempfile.TemporaryDirectory() as src_dir_name, tempfile.TemporaryDirectory() as dst_dir_name:
        src = Path(src_dir_name) / "gamedir" / "mysavesrc"
        dst = Path(dst_dir_name) / "mysavedst"

        # run ssf
        ssf.files.symlink(src, dst)

        assert src.exists() is False
        assert (dst / "save.txt").exists() is False
