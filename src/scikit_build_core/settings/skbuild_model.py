import dataclasses
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from .._compat.typing import Annotated, Literal

__all__ = [
    "BackportSettings",
    "CMakeSettings",
    "EditableSettings",
    "GenerateSettings",
    "InstallSettings",
    "BuildSettings",
    "LoggingSettings",
    "NinjaSettings",
    "SDistSettings",
    "ScikitBuildSettings",
    "WheelSettings",
]


def __dir__() -> List[str]:
    return __all__


@dataclasses.dataclass
class CMakeSettings:
    minimum_version: Optional[Version] = None
    """
    DEPRECATED in 0.8; use version instead.
    """

    version: SpecifierSet = SpecifierSet(">=3.15")
    """
    The versions of CMake to allow. If CMake is not present on the system or does
    not pass this specifier, it will be downloaded via PyPI if possible. An empty
    string will disable this check.
    """

    args: List[str] = dataclasses.field(default_factory=list)
    """
    A list of args to pass to CMake when configuring the project. Setting this
    in config or envvar will override toml. See also ``cmake.define``.
    """

    define: Annotated[Dict[str, Union[str, bool]], "EnvVar"] = dataclasses.field(
        default_factory=dict
    )
    """
    A table of defines to pass to CMake when configuring the project. Additive.
    """

    verbose: bool = False
    """
    Verbose printout when building.
    """

    build_type: str = "Release"
    """
    The build type to use when building the project.
    Valid options are: "Debug", "Release", "RelWithDebInfo", "MinSizeRel",
    "", etc.
    """

    source_dir: Path = Path()
    """
    The source directory to use when building the project. Currently only
    affects the native builder (not the setuptools plugin).
    """

    targets: List[str] = dataclasses.field(default_factory=list)
    """
    The build targets to use when building the project. Empty builds the
    default target.
    """


@dataclasses.dataclass
class NinjaSettings:
    minimum_version: Optional[Version] = None
    """
    DEPRECATED in 0.8; use version instead.
    """

    version: SpecifierSet = SpecifierSet(">=1.5")
    """
    The versions of Ninja to allow. If Ninja is not present on the system or does
    not pass this specifier, it will be downloaded via PyPI if possible. An empty
    string will disable this check.
    """

    make_fallback: bool = True
    """
    If Ninja is not present on the system or is older than required,
    it will be downloaded via PyPI if this is false.
    """


@dataclasses.dataclass
class LoggingSettings:
    level: Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        "WARNING"
    )
    """
    The logging level to display, "DEBUG", "INFO", "WARNING", and "ERROR" are
    possible options.
    """


@dataclasses.dataclass
class SDistSettings:
    include: List[str] = dataclasses.field(default_factory=list)
    """
    Files to include in the SDist even if they are skipped by default.
    Supports gitignore syntax.

    """

    exclude: List[str] = dataclasses.field(default_factory=list)
    """
    Files to exclude from the SDist even if they are included by default.
    Supports gitignore syntax.
    """

    reproducible: bool = True
    """
    If set to True, try to build a reproducible distribution (Unix and Python
    3.9+ recommended).  ``SOURCE_DATE_EPOCH`` will be used for timestamps, or a
    fixed value if not set.
    """

    cmake: bool = False
    """
    If set to True, CMake will be run before building the SDist.
    """


@dataclasses.dataclass
class WheelSettings:
    packages: Optional[List[str]] = None
    """
    A list of packages to auto-copy into the wheel. If this is not set, it will
    default to the first of ``src/<package>``, ``python/<package>``, or
    ``<package>`` if they exist.  The prefix(s) will be stripped from the
    package name inside the wheel.
    """

    py_api: str = ""
    """
    The Python tags. The default (empty string) will use the default Python
    version. You can also set this to "cp37" to enable the CPython 3.7+ Stable
    ABI / Limited API (only on CPython and if the version is sufficient,
    otherwise this has no effect). Or you can set it to "py3" or "py2.py3" to
    ignore Python ABI compatibility. The ABI tag is inferred from this tag.
    """

    expand_macos_universal_tags: bool = False
    """
    Fill out extra tags that are not required. This adds "x86_64" and "arm64"
    to the list of platforms when "universal2" is used, which helps older
    Pip's (before 21.0.1) find the correct wheel.
    """

    install_dir: str = ""
    """
    The install directory for the wheel. This is relative to the platlib root.
    You might set this to the package name. The original dir is still at
    SKBUILD_PLATLIB_DIR (also SKBUILD_DATA_DIR, etc. are available).
    EXPERIMENTAL: An absolute path will be one level higher than the platlib
    root, giving access to "/platlib", "/data", "/headers", and "/scripts".
    """

    license_files: List[str] = dataclasses.field(
        default_factory=lambda: ["LICEN[CS]E*", "COPYING*", "NOTICE*", "AUTHORS*"]
    )
    """
    A list of license files to include in the wheel. Supports glob patterns.
    """

    cmake: bool = True
    """
    If set to True (the default), CMake will be run before building the wheel.
    """

    platlib: Optional[bool] = None
    """
    Target the platlib or the purelib. If not set, the default is to target the
    platlib if wheel.cmake is true, and the purelib otherwise.
    """

    exclude: List[str] = dataclasses.field(default_factory=list)
    """
    A set of patterns to exclude from the wheel. This is additive to the SDist
    exclude patterns. This applies to the final paths in the wheel, and can
    exclude files from CMake output as well.  Editable installs may not respect
    this exclusion.
    """

    build_tag: str = ""
    """
    The build tag to use for the wheel. If empty, no build tag is used.
    """


@dataclasses.dataclass
class BackportSettings:
    find_python: Version = Version("3.26.1")
    """
    If CMake is less than this value, backport a copy of FindPython. Set to 0
    disable this, or the empty string.
    """


@dataclasses.dataclass
class EditableSettings:
    mode: Literal["redirect", "inplace"] = "redirect"
    """
    Select the editable mode to use. Can be "redirect" (default) or "inplace".
    """

    verbose: bool = True
    """
    Turn on verbose output for the editable mode rebuilds.
    """

    rebuild: bool = False
    """
    Rebuild the project when the package is imported. The build-directory must
    be set.
    """


@dataclasses.dataclass
class BuildSettings:
    tool_args: List[str] = dataclasses.field(default_factory=list)
    """
    Extra args to pass directly to the builder in the build step.
    """


@dataclasses.dataclass
class InstallSettings:
    components: List[str] = dataclasses.field(default_factory=list)
    """
    The components to install. If empty, all default components are installed.
    """

    strip: Optional[bool] = None
    """
    Whether to strip the binaries. True for scikit-build-core 0.5+.
    """


@dataclasses.dataclass
class GenerateSettings:
    path: Path
    """
    The path (relative to platlib) for the file to generate.
    """

    template: str = ""
    """
    The template to use for the file. This includes string.Template style
    placeholders for all the metadata. If empty, a template-path must be set.
    """

    template_path: Optional[Path] = None
    """
    The path to the template file. If empty, a template must be set.
    """

    location: Literal["install", "build", "source"] = "install"
    """
    The place to put the generated file. The "build" directory is useful for
    CMake files, and the "install" directory is useful for Python files,
    usually. You can also write directly to the "source" directory, will
    overwrite existing files & remember to gitignore the file.
    """


@dataclasses.dataclass
class ScikitBuildSettings:
    cmake: CMakeSettings = dataclasses.field(default_factory=CMakeSettings)
    ninja: NinjaSettings = dataclasses.field(default_factory=NinjaSettings)
    logging: LoggingSettings = dataclasses.field(default_factory=LoggingSettings)
    sdist: SDistSettings = dataclasses.field(default_factory=SDistSettings)
    wheel: WheelSettings = dataclasses.field(default_factory=WheelSettings)
    backport: BackportSettings = dataclasses.field(default_factory=BackportSettings)
    editable: EditableSettings = dataclasses.field(default_factory=EditableSettings)
    build: BuildSettings = dataclasses.field(default_factory=BuildSettings)
    install: InstallSettings = dataclasses.field(default_factory=InstallSettings)
    generate: List[GenerateSettings] = dataclasses.field(default_factory=list)

    metadata: Dict[str, Dict[str, Any]] = dataclasses.field(default_factory=dict)
    """
    List dynamic metadata fields and hook locations in this table.
    """

    strict_config: bool = True
    """
    Strictly check all config options. If False, warnings will be
    printed for unknown options. If True, an error will be raised.
    """

    experimental: bool = False
    """
    Enable early previews of features not finalized yet.
    """

    minimum_version: Optional[Version] = None
    """
    If set, this will provide a method for backward compatibility.
    """

    build_dir: str = ""
    """
    The build directory. Defaults to a temporary directory, but can be set.
    """
