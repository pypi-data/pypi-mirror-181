from hestia_earth.schema import PracticeStatsDefinition, TermTermType

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.practice import _new_practice
from .utils import (
    MAX_AREA_SIZE, download, get_region_factor, has_geospatial_data, should_download
)
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "site": {
            "@type": "Site",
            "or": [
                {"latitude": "", "longitude": ""},
                {"boundary": {}},
                {"region": {"@type": "Term", "termType": "region"}}
            ]
        }
    }
}
RETURNS = {
    "Practice": [{
        "value": "",
        "statsDefinition": "spatial"
    }]
}
LOOKUPS = {
    "region-landUseManagement": "croppingIntensity"
}
TERM_ID = 'croppingIntensity'
EE_PARAMS = {
    'ee_type': 'raster',
    'reducer': 'sum',
    'fields': 'sum'
}


def _practice(value: float):
    practice = _new_practice(TERM_ID, MODEL)
    practice['value'] = [round(value, 7)]
    practice['statsDefinition'] = PracticeStatsDefinition.SPATIAL.value
    return practice


def _download(site: dict):
    # 1) extract maximum monthly growing area (MMGA)
    MMGA_value = download(
        TERM_ID,
        site,
        {
            **EE_PARAMS,
            'collection': 'MMGA'
        }
    )
    MMGA_value = MMGA_value.get(EE_PARAMS['reducer'], 0)

    # 2) extract area harvested (AH)
    AH_value = download(
        TERM_ID,
        site,
        {
            **EE_PARAMS,
            'collection': 'AH'
        }
    )
    AH_value = AH_value.get(EE_PARAMS['reducer'])

    # 3) estimate croppingIntensity from MMGA and AH.
    return None if MMGA_value is None or AH_value is None or AH_value == 0 else (MMGA_value / AH_value)


def _run(site: dict):
    value = _download(site)
    return [_practice(value)] if value is not None else []


def _run_default(site: dict):
    region_factor = get_region_factor(TERM_ID, site, TermTermType.LANDUSEMANAGEMENT)

    logRequirements(site, model=MODEL, term=TERM_ID,
                    region_factor=region_factor)

    should_run = all([region_factor])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return [_practice(region_factor)] if should_run else []


def _should_run(site: dict):
    geospatial_data = has_geospatial_data(site)
    below_max_area_size = should_download(site)

    logRequirements(site, model=MODEL, term=TERM_ID,
                    geospatial_data=geospatial_data,
                    max_area_size=MAX_AREA_SIZE,
                    below_max_area_size=below_max_area_size)

    should_run = all([geospatial_data, below_max_area_size])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return should_run


def run(cycle: dict):
    site = cycle.get('site')
    return _run(site) if _should_run(site) else _run_default(site)
