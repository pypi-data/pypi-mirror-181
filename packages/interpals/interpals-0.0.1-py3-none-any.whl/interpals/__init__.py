__title__ = 'interpals'
__author__ = 'cynical'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Cynical'
__version__ = '0.0.1'
__description__ = 'A Python wrapper for the Interpals API'

from httpx import get
latestVersion = get("https://pypi.org/pypi/interpals/json").json()["info"]["version"]

if __version__ != latestVersion:
    print(f"WARNING: You are using an outdated version of interpals. The latest version is {latestVersion}.")
