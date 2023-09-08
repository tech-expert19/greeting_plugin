# coding=utf-8
# pylint: disable=open-builtin
import io
import os
from setuptools import find_packages, setup
from typing import Dict, List

HERE = os.path.abspath(os.path.dirname(__file__))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def load_readme() -> str:
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        readme = f.read()
    return readme


def load_about() -> Dict[str, str]:
    about: Dict[str, str] = {}
    with io.open(os.path.join(HERE, "__about__.py"), "rt", encoding="utf-8") as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()

print("Found packages: {packages}".format(packages=find_packages()))

setup(
    name="greeting-plugin",
    version=ABOUT["__package_version__"],
    packages=find_packages(),
    package_data={"": ["*.html"]},  # include any Mako templates found in this repo.
    include_package_data=True,
    license_files=("LICENSE.txt",),
    license="AGPLv3",
    description="Django plugin to add greeting REST API endpoint in Open edX platform.",
    long_description=load_readme(),
    author="Raza Fayyaz",
    author_email="raza.fayyaz.rf@gmail.com",
    url="https://github.com/tech-expert19/greeting_plugin.git",
    download_url=("https://github.com/tech-expert19/greeting_plugin.git"),
    zip_safe=False,
    keywords="Django, Open edX, Plugin",
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
    ],
    entry_points={
        "lms.djangoapp": [
            "greeting_plugin = greeting_plugin.apps:GreetingPluginAPIConfig"
        ]
    },
    extras_require={
        "Django": ["Django>=3.2"],
    },
)
