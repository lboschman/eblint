from .field_order_checker import FieldOrderChecker
from .mandatory_field_checker import MandatoryFieldChecker
from .last_field_checker import LastFieldChecker


_default_mandatory_field_checker = MandatoryFieldChecker(
    issue_code="M001",
    field_names=[
        "easyblock",
        "name",
        "version",
        "homepage",
        "description",
        "dependencies",
        "builddependencies",
        "toolchain",
    ],
)

_default_first_fields_checker = FieldOrderChecker(
    "M002",
    field_names=["easyblock", "name", "version", "versionsuffix"],
    strict_mode=True,
)

_default_field_order_checker = FieldOrderChecker(
    issue_code="M003",
    field_names=[
        "versionsuffix",
        "homepage",
        "description",
        "toolchain",
        "toolchainopts",
        "github_account",
        "source_urls",
        "sources",
        "download_instructions",
        "patches",
        "crates",
        "checksums",
        "osdependencies",
        "allow_system_deps",
        "builddependencies",
        "dependencies",
        "start_dir",
        "preconfigopts",
        "configopts",
        "prebuildopts",
        "buildopts",
        "preinstallopts",
        "installopts",
        "runtest",
        "postintallcmds",
        "fix_python_shebang_for",
        "exts_list",
        "sanity_check_paths",
        "sanity_check_commands",
        "modextravars",
        "modluafooter",
        "modtclfootar",
        "moduleclass",
    ],
)

_default_last_field_checker = LastFieldChecker("M004", last_field_name="moduleclass")

DEFAULT_CHECKERS = {
    _default_mandatory_field_checker,
    _default_first_fields_checker,
    _default_field_order_checker,
    _default_last_field_checker,
}
