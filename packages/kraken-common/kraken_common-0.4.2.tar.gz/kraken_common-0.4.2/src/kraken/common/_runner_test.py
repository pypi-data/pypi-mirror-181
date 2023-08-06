from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Iterator

from pytest import fixture

from kraken.common._buildscript import BuildscriptMetadata
from kraken.common._runner import BuildDslScriptRunner, PythonScriptRunner


@fixture
def tempdir() -> Iterator[Path]:
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test__PythonScriptRunner__can_find_and_execute_script(tempdir: Path) -> None:
    (tempdir / "kraken.py").write_text(
        dedent(
            """
        from kraken.common import buildscript

        buildscript(requirements=["kraken-std"])
        """
        )
    )
    runner = PythonScriptRunner()
    script = runner.find_script(tempdir)
    assert script is not None

    with BuildscriptMetadata.capture() as metadata_future:
        runner.execute_script(script, {})

    assert metadata_future.result() == BuildscriptMetadata(requirements=["kraken-std"])


def test__BuildDslScriptRunner__can_find_and_execute_script(tempdir: Path) -> None:
    (tempdir / "kraken.build").write_text(
        dedent(
            """
        buildscript {
            requires "kraken-std"
        }
        """
        )
    )

    runner = BuildDslScriptRunner()
    script = runner.find_script(tempdir)
    assert script is not None

    with BuildscriptMetadata.capture() as metadata_future:
        runner.execute_script(script, {})

    assert metadata_future.result() == BuildscriptMetadata(requirements=["kraken-std"])
