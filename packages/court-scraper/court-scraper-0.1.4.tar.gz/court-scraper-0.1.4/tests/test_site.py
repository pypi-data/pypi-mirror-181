import pytest

from court_scraper import Site

from .conftest import CAPTCHA_API_KEY, update_test_configs


@pytest.mark.parametrize(
    "place_id,site_class",
    [
        ("ga_dekalb", "Site"),
        ("ok_tulsa", "Site"),
        ("wi_milwaukee", "Site"),
    ],
)
@pytest.mark.slow
@pytest.mark.nocaptcha
@pytest.mark.usefixtures("set_env", "create_scraper_dir", "create_config")
def test_site(place_id, site_class):
    site = Site(place_id)
    assert site.__class__.__name__ == site_class


@pytest.mark.webtest
@pytest.mark.slow
@pytest.mark.nocaptcha
@pytest.mark.usefixtures("create_scraper_dir", "create_config")
def test_site_odyssey(headless):
    site = Site("ca_napa", headless=headless)
    case_numbers = ["20CV000569"]
    results = site.search(case_numbers)
    assert len(results) == 1


@pytest.mark.webtest
@pytest.mark.slow
@pytest.mark.captcha
@pytest.mark.usefixtures("set_env", "create_scraper_dir", "create_config")
def test_site_wicourts(config_path, headless):
    # Add captcha key to test config file in order to
    # test automatic lookup of CAPTCHA api key
    update_test_configs(config_path, {"captcha_service_api_key": CAPTCHA_API_KEY})
    site = Site("wi_green_lake")
    case_numbers = ["2021CV000055"]
    results = site.search(case_numbers=case_numbers, headless=headless)
    assert len(results) == 1


@pytest.mark.vcr()
def test_site_ok():
    # Test a case number search
    tulsa = Site("ok_tulsa")
    case_numbers = ["CJ-2021-1904"]
    results = tulsa.search(case_numbers=case_numbers)
    assert len(results) == 1


@pytest.mark.vcr()
def test_by_date_tulsa():
    # Test a date search on a country with a dedicated daily filings page
    tulsa = Site("ok_tulsa")
    tulsa.search_by_date()


# @pytest.mark.vcr()
# def test_by_date_kiowa():
#     # Test a date search on a county without one
#     kiowa = Site("ok_kiowa")
#     kiowa.search_by_date()
