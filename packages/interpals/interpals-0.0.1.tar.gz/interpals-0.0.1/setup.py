from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()
requirements = ["httpx", "websocket-client==1.4.1", "websockets==10.3"]

setup(
    name="interpals",
    license='MIT',
    author="forevercynical",
    version="0.0.1",
    author_email="me@cynical.gg",
    description="Interpals API wrapper to make bots easier to use",
    url="https://github.com/forevercynical/interpals",
    packages=find_packages(),
    long_description = long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    keywords=[
        'interpals', 'interpals-bot', 'interpals-bots'
    ],
    python_requires='>=3.6',
)
