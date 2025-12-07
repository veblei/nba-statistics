from pathlib import Path

import pytest


@pytest.fixture
def my_dir():
    return Path(__file__).parent.parent.resolve()


def test_location(my_dir):
    # check that we're in repo root/my_dir
    assert (
        my_dir.name == "nba-statistics"
    ), "Project is not in the correct directory!"


@pytest.mark.parametrize(
    "filename",
    [
        "README.md",
        "requesting_urls.py",
        "filter_urls.py",
        "collect_dates.py"
    ],
)
def test_files_exist(my_dir, filename):
    assert my_dir.joinpath(filename).exists()
