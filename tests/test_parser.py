import os
import json
from unittest.mock import patch

import pytest
import vcr

from greasyfork_archive import main_wrapper

this_dir = os.path.abspath(os.path.dirname(__file__))
out_file = os.path.join(this_dir, "out.json")


@patch("time.sleep", return_value=None)
@vcr.use_cassette("tests/vcr_cassettes/response.yaml")
def test_response(patched_sleep):
    main_wrapper(96096, out_file)
    with open(out_file) as json_dump:
        jscripts = json.load(json_dump)
    scripts = jscripts["greasyfork_scripts"]
    assert isinstance(scripts, list)
    assert len(scripts) == 20
    first_entry = scripts[0]
    assert first_entry["script_name"] == "MyAnimeList Remove Unnecessary Spacing"
    assert first_entry["daily_installs"] == 1
    assert first_entry["total_installs"] == 108
    assert first_entry["rating_score"] == 5.0
    assert first_entry["created_date"] == '2017-01-19'
    assert first_entry["updated_date"] == '2019-02-01'
    assert first_entry["script_type"] == 'public'
    assert first_entry["script_version"] == "1.0.3"
    assert first_entry["sensitive"] == False
    assert first_entry["language"] == 'js'
    assert first_entry["css_available_as_js"] == False
    assert first_entry["url"] == 'https://greasyfork.org//en/scripts/26678-myanimelist-remove-unnecessary-spacing'
    assert ".user-profile-about" in first_entry["code"]


