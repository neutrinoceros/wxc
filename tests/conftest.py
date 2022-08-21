import os
from pathlib import Path

import pytest

packages_to_try = [
    # stdlib
    "math",
    "platform",
    "uuid",
    "fractions",
    # common third party
    "numpy",
    "matplotlib",
    "pandas",
    "requests",
    "django",
    "flask",
    "IPython",
    "tqdm",
]


@pytest.fixture(params=packages_to_try)
def package_name(request):
    return request.param


SHARED_DATA_DIR = Path(__file__).with_name("data")


@pytest.fixture()
def fake_module(monkeypatch):
    fake_module = SHARED_DATA_DIR / "fake_empty_module"

    syspath, name = fake_module.parent, fake_module.name
    monkeypatch.syspath_prepend(syspath)
    yield syspath, name


def pytest_configure():
    # minimal workaround to avoid false negatives when testing
    # with rich installed.
    os.environ.update({"COLUMNS": "90"})
