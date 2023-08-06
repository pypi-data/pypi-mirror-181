import importlib.metadata


_package_name = 'fish-databricks-jobs'


def _package_version():
    try:
        _result = importlib.metadata.version(_package_name)
    except importlib.metadata.PackageNotFoundError:
        _result = 'no-version'
    return _result


package_version = _package_version()
