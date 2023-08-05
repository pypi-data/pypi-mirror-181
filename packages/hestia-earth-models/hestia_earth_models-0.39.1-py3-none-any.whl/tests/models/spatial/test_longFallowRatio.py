from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_practice

from hestia_earth.models.spatial.longFallowRatio import MODEL, TERM_ID, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}.has_geospatial_data")
def test_should_run(mock_has_geospatial_data, *args):
    mock_has_geospatial_data.return_value = True
    assert _should_run({})

    mock_has_geospatial_data.return_value = False
    assert not _should_run({})


@patch(f"{class_path}._new_practice", side_effect=fake_new_practice)
@patch(f"{class_path}.download", return_value={})
def test_run(mock_download, *args):
    with open(f"{fixtures_path}/{MODEL}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    run({'site': site})
    assert mock_download.call_count == 2
