from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("{{cookiecutter.project_name}}")
except PackageNotFoundError:
    __version__ = "{{cookiecutter.version}}"

if __name__ == "__main__":
    print(__version__)
