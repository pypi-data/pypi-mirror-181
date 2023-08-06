"""Errors specific to this library."""


from dataclasses import KW_ONLY, dataclass
from typing import Optional

from dbnomics_data_model import DatasetCode, ProviderCode
from solrq import Q

from dbnomics_solr.types import SolrDoc

__all__ = [
    "DatasetAlreadyIndexed",
    "DatasetNotFound",
    "DBnomicsSolrException",
    "DuplicateDocuments",
    "IndexationError",
    "InvalidSolrDocument",
    "ProviderNotFound",
]


class DBnomicsSolrException(Exception):
    pass


@dataclass
class DatasetAlreadyIndexed(DBnomicsSolrException):
    provider_code: ProviderCode
    dataset_code: DatasetCode
    dir_hash: str


@dataclass
class DatasetNotFound(DBnomicsSolrException):
    provider_code: ProviderCode
    dataset_code: DatasetCode


@dataclass
class DuplicateDocuments(DBnomicsSolrException):
    query: Q


@dataclass
class InvalidSolrDocument(DBnomicsSolrException):
    message: str = "Invalid Solr document"
    _: KW_ONLY
    solr_document: SolrDoc

    def __str__(self):
        return self.message


@dataclass
class ProviderNotFound(DBnomicsSolrException):
    provider_slug: Optional[str] = None


@dataclass
class IndexationError(DBnomicsSolrException):
    error: Optional[dict] = None

    def __str__(self):
        return str(self.error)
