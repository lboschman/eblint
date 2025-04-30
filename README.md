# An easybuild config linter

Eblint is a linter for [easybuild config files](https://docs.easybuild.io/writing-easyconfig-files/).
It uses the Python standard library `ast` module to parse the config files,
as those files follow Python syntax.

## Installation

Install `eblint` with `pip`:

```bash
pip install eblint
```

## Usage

You can lint an individual config file with by invoking `eblint` on the command line.
Eblint also supports multiple input files and wildcards.
The following are all valid calls to `eblint`:

```bash
eblint example-config.eb
eblint example-config-1.eb example-config-2.eb
eblint **/*.eb
```

## Current rules

Eblint is aimed at closely resembling the specifications laid out by Easybuild.
Currently the following rules are in place

### M001: Mandatory fields

The following fields are required

```txt
easyblock
name
version
homepage
description
dependencies
builddependencies
toolchain
```

### M002: First ordered fields

The first fields in a config file are the ones below, in that particular order.
Other fields cannot be defined before or in between those fields.

```txt
easyblock
name
version
versionsuffix
```

### M003: Soft ordered fields

The following fields are required to be in this order.
Other fields not mentioned in this list can come before or in between, but
the fields in this list are required to be in this order.

```txt
versionsuffix
homepage
description
toolchain
toolchainopts
github_account
source_urls
sources
download_instructions
patches
crates
checksums
osdependencies
allow_system_deps
builddependencies
dependencies
start_dir
preconfigopts
configopts
prebuildopts
buildopts
preinstallopts
installopts
runtest
postintallcmds
fix_python_shebang_for
exts_list
sanity_check_paths
sanity_check_commands
modextravars
modluafooter
modtclfootar
moduleclass
```

### M004: Final field

The last field in an easybuild config file should be `moduleclass`.
