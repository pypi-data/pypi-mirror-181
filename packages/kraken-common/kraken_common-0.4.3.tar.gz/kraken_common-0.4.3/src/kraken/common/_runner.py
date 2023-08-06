"""
Implements build script runners.
"""

import re
import types
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterator, Sequence, Tuple

import builddsl

from ._buildscript import BuildscriptMetadata, buildscript


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

    @abstractmethod
    def has_buildscript_call(self, script: Path) -> bool:
        """
        Implement a heuristic to check if the script implements a call to the :func:`buildscript` function.
        """

        raise NotImplementedError(self)

    @abstractmethod
    def get_buildscript_call_recommendation(self, metadata: BuildscriptMetadata) -> str:
        """
        Make a recommendation to the user for the code the user should put into their build script for the
        :func:`buildscript` call that is required by Kraken wrapper.
        """

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
        module = types.ModuleType(str(script.parent))
        module.__file__ = str(script)

        code = compile(script.read_text(), script, "exec")
        exec(code, vars(module))

    def has_buildscript_call(self, script: Path) -> bool:
        code = script.read_text()
        if not re.search(r"^from kraken.common import buildscript", code, re.M):
            return False
        if not re.search(r"^buildscript\s*\(", code, re.M):
            return False
        return True

    def get_buildscript_call_recommendation(self, metadata: BuildscriptMetadata) -> str:
        code = "from kraken.common import buildscript\nbuildscript("
        if metadata.index_url:
            code += f"\n    index_url={metadata.index_url!r},"
        if metadata.extra_index_urls:
            if len(metadata.extra_index_urls) == 1:
                code += f"\n    extra_index_urls={metadata.extra_index_urls!r},"
            else:
                code += "\n    extra_index_urls=["
                for url in metadata.extra_index_urls:
                    code += f"\n        {url!r},"
                code += "\n    ],"
        if metadata.requirements:
            if sum(map(len, metadata.requirements)) < 50:
                code += f"\n    requirements={metadata.requirements!r},"
            else:
                code += "\n    requirements=["
                for req in metadata.requirements:
                    code += f"\n        {req!r},"
                code += "\n    ],"
        if not code.endswith("("):
            code += "\n"
        code += ")"
        return code


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

    def has_buildscript_call(self, script: Path) -> bool:
        code = script.read_text()
        if re.match(r"^buildscript\s*(\(|\{})", code, re.M):
            return False
        return True

    def get_buildscript_call_recommendation(self, metadata: BuildscriptMetadata) -> str:
        code = "buildscript {"
        if metadata.index_url:
            code += f"\n    index_url = {metadata.index_url!r}"
        if metadata.extra_index_urls:
            for url in metadata.extra_index_urls:
                code += f"\n    extra_index_url {url!r}"
        if metadata.requirements:
            for req in metadata.requirements:
                code += f"        requires {req!r}"
        code += "}"
        return code


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
