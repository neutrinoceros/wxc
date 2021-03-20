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
    "toml",
]


@pytest.fixture(params=packages_to_try)
def package_name(request):
    return request.param
