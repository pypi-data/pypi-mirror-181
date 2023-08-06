"""Domain-level service to delete data related to a dataset."""

import daiquiri
from dbnomics_data_model import ProviderCode
from humanfriendly.text import pluralize
from pysolr import Results

from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["search_provider_datasets"]


logger = daiquiri.getLogger(__name__)


def search_provider_datasets(provider_code: ProviderCode, *, dbnomics_solr_client: DBnomicsSolrClient) -> Results:
    """Search the dataset documents related to that provider."""
    results = dbnomics_solr_client.search_provider_datasets(provider_code)
    if results.hits == 0:
        logger.debug("No dataset documents were found for that provider", provider_code=provider_code)
    else:
        logger.debug(
            "Found %s for that provider", pluralize(results.hits, "dataset document"), provider_code=provider_code
        )
    return results
