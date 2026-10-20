"""Shared file preflight for the offline command-line tools."""

from pathlib import Path
import os
import tempfile


def validate_outputs(inputs=(), outputs=(), *, force=False):
    """Reject source aliases, duplicate destinations and accidental overwrites.

    Existing outputs require an explicit CLI --force. Source files are protected
    even with --force, including symlinks and existing hard links.
    """
    if type(force) is not bool:
        raise TypeError("force must be a boolean")
    sources = [Path(p).resolve() for p in inputs if p is not None]
    destinations = []
    for value in outputs:
        if value is None:
            continue
        path = Path(value).resolve()
        if not path.parent.is_dir():
            raise ValueError(f"Output parent directory does not exist: {path.parent}")
        for other in sources + destinations:
            if path == other or (path.exists() and other.exists() and os.path.samefile(path, other)):
                raise ValueError(f"Output aliases an input or another output: {value}")
        if path.exists() and (not path.is_file() or not force):
            raise ValueError(f"Output already exists (choose a new path or use --force): {value}")
        destinations.append(path)


def command_inputs(args):
    inputs = []
    for name in ("input", "binary", "code", "object", "resource_map"):
        value = getattr(args, name, None)
        if value:
            inputs.append(value)
    inputs.extend(getattr(args, "inputs", ()))
    inputs.extend(getattr(args, "objects", ()))
    return inputs


def write_output(path, data, *, inputs=(), force=False):
    """Exclusive by default; explicit replacement never truncates link targets."""
    if not isinstance(data, (str, bytes, bytearray)):
        raise TypeError("output data must be str, bytes or bytearray")
    validate_outputs(inputs, [path], force=force)
    payload = data.encode("utf-8") if isinstance(data, str) else data
    if not force:
        identity = None
        try:
            with open(path, "xb") as stream:
                created = os.fstat(stream.fileno())
                identity = (created.st_dev, created.st_ino)
                stream.write(payload)
        except BaseException:
            if identity is not None:
                try:
                    current = os.stat(path, follow_symlinks=False)
                    if (current.st_dev, current.st_ino) == identity:
                        os.unlink(path)
                except OSError:
                    pass  # Retain original failure; externally replaced paths stay intact.
            raise
        return
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=Path(path).parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
        validate_outputs(inputs, [path], force=True)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_command_output(args, path, data):
    write_output(path, data, inputs=command_inputs(args), force=getattr(args, "force", False))


def validate_command_outputs(args):
    """Preflight direct and derived filenames before any command writes."""
    command = getattr(args, "command", "compile")
    inputs = command_inputs(args)
    output = getattr(args, "output", None)
    if command in ("compile", "asm-object") and hasattr(args, "module") and not output:
        output = str(Path(args.input).with_suffix(".k11o"))
    if command == "patch" and not output:
        src = Path(args.binary)
        output = str(src.with_name(src.stem + "_patched" + src.suffix))
    if command == "checksum" and getattr(args, "fix", False) and not output:
        src = Path(args.input)
        output = str(src.with_name(src.stem + "_checksum" + src.suffix))
        args.output = output
    validate_outputs(inputs, [output, getattr(args, "map_out", None)], force=getattr(args, "force", False))
