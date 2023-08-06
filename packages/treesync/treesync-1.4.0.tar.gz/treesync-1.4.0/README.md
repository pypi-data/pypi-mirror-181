![Unit Tests](https://github.com/hile/treesync/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/treesync/actions/workflows/lint.yml/badge.svg)

# Tree synchronization utility

This utility allows configuring regularly repeated rsync commands and sharing
of configuration flags per server. Configured *sync targets* can be called
with `treesync pull` and `treesync push` commands to avoid mistakes in repeated
long and complex rsync arguments.


# Example usage

Following example commands show how to use the tool for listing and syncing multiple targets.

These example commands match the example configuration shown below.

```bash
# List all targets
> treesync list
laptop:music
nas:documents
nas:music

# Lists targets where host or target name starts with letter s or m
> treesync list s* m*
laptop:music
nas:music

# Pull documents files from nas server
> treesync pull nas-server:documents

# Push music to bot nas-server and laptop
> treesync push music

# Push all files to nas-server
> treesync push nas-server
```

# Installing

Install latest version from *pypi*:

```bash
pip install treesync
```

# Configuration file

Configuration file for treesync tool is `~/.config/treesync.yml`. The file suppports defining sync targets in two formats. Both formats can be mixed in same configuration file.

If same target name is defined in both formats, the `sources and hosts` declaration is used.

## Sources and hosts format

The `sources` and `hosts` format contains two sections:

- `sources` list of dictionaries with `name` and  `path` elements and with optional `excludes_file`
   option
- `hosts` list of dictionaries with at least `name` and `targets` options and with optional
  `iconv`, `rsync_path` and `flags` options

This format is suitable to use when same source is pushed to multiple target servers: the format
defines source path and excludes file in one place and avoids copypaste errors.

Example configuration with all supported flags:

```yaml
hosts:
  # macOS laptop with 'rsync 3' from homebrew
  - name: laptop
    # Defines the rsync command path on remote host (from macOS homebrew)
    rsync_path: /usr/local/bin/rsync
    targets:
      # Listed as laptop:music
      - source: music
        # The laptop is also a Mac, so no iconv is needed
        destination: mylaptop:/Users/myname/Music
  # Demo host with Linux or FreeBSD, requiring the 'iconv' config
  - name: nas
    # This is rsync flag to push from macOS to Linux/BSD
    iconv: UTF-8-MAC,UTF-8
    # Remove server will have different username
    flags:
      - --usermap=localuser:nasuser
      - --groupmap=localgroup:nasgroup
    targets:
      # The source field refers to 'sources' section name field
      # Listed as nas:documents
      - source: documents
        # Destination is full rsync command remote path without any special quoting
        destination: nas-server:/backups/My Documents
      # Listed as nas:music
      - source: music
        destination: nas-server:/shared/Music
sources:
  - name: documents
    path: /Users/myname/Documents
    excludes_file: /Users/myname/Documents/.rsync_exclude
  - name: music
    path: /Users/myname/Music
    excludes_file: /Users/myname/.music-excluded
```

## Targets format

The `targets` format defines sync targets with `targets` with a single configuration section
and server specific settings with `servers` section. In this format, the excludes_file must be
repeated for each 'source' and source paths are repeated if pushed to multiple servers.

This format is suitable for cases where the same source is not pushed to multiple targets.

Server name to get server settings from `servers`section is recognized from the `destination`
field path by separating the path from first `:` letter.

```yaml
servers:
  laptop:
    # Defines the rsync command path on remote host
    rsync_path: /usr/local/bin/rsync
  nas-server:
    # This is rsync flag to push from macOS to Linux/BSD
    iconv: UTF-8-MAC,UTF-8
    # Remove server will have different username
    flags:
      - --usermap=localuser:remoteuser
      - --groupmap=localgroup:users
targets:
  nas:documents:
    source: /Users/localuser/Documents
    destination: nas-server:/shared/Music
    excludes_file: /home/localuser/Documents/.rsync_exclude
  nas:music:
    source: /Users/localuser/Music
    destination: nas-server:/shared/Music
    excludes_file: /Users/myname/.music-excluded
  laptop:music:
    source: /Users/localuser/Music
    destination: nas-server:/shared/Music
    excludes_file: /Users/myname/.music-excluded
```

Examples of valid configuration files can be also seen in unit test data:

* [sources and hosts configuration](tests/mock/host_sources.yml)
* [old format target list configuration](tests/mock/old_format_servers.yml)
