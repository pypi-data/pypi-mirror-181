"""
Implements build script runners.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterator, Sequence, Tuple

import builddsl

from ._buildscript import buildscript


class ScriptRunner(ABC):
    """
    Abstract class for script runners. Implementations of this class are used to detect a script in a directory
    and to actually run it. The Kraken wrapper and build system both use this to run a build script, which for
    the wrapper is needed to extract the build script metadata.
    """

    @abstractmethod
    def find_script(self, directory: Path) -> "Path | None":
        raise NotImplementedError(self)

    @abstractmethod
    def execute_script(self, script: Path, scope: Dict[str, Any]) -> None:
        raise NotImplementedError(self)


class ScriptFinder(ScriptRunner):
    """
    Base class for finding script files in a directory based on a few criteria.
    """

    def __init__(self, filenames: Sequence[str]) -> None:
        self.filenames = list(filenames)

    def find_script(self, directory: Path) -> "Path | None":
        for filename in self.filenames:
            script = directory / filename
            if script.is_file():
                return script
        return None


class PythonScriptRunner(ScriptFinder):
    """
    A finder and runner for Python based Kraken build scripts called `kraken.py` (optionally prefixed with `.`).
    """

    def __init__(self, filenames: Sequence[str] = ("kraken.py", ".kraken.py")) -> None:
        super().__init__(filenames)

    def execute_script(self, script: Path, scope: Dict[str, Any]) -> None:
        code = compile(script.read_text(), script, "exec")
        exec(code, scope)


class BuildDslScriptRunner(ScriptFinder):
    """
    A finder and runner for BuildDSL based Kraken build scripts called `kraken.build` (optionally prefixed with `.`).
    """

    def __init__(self, filenames: Sequence[str] = ("kraken.build", ".kraken.build")) -> None:
        super().__init__(filenames)

    def execute_script(self, script: Path, scope: Dict[str, Any]) -> None:
        code = script.read_text()
        scope = {"buildscript": buildscript, **scope}
        builddsl.Closure.from_map(scope).run_code(code, str(script))


def iter_script_runners() -> Iterator[ScriptRunner]:
    """
    Iterate over all available script runners.
    """

    yield PythonScriptRunner()
    yield BuildDslScriptRunner()


def find_build_script(directory: Path) -> "Tuple[ScriptRunner, Path] | Tuple[None, None]":
    """
    Searches for a supported build script in the given *directory* and returns the matching :class:`ScriptRunner`
    and filename.
    """

    for runner in iter_script_runners():
        script = runner.find_script(directory)
        if script is not None:
            return runner, script

    return None, None
