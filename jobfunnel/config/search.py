"""Object to contain job query metadata
"""
from typing import List, Optional
from jobfunnel.config import BaseConfig
from jobfunnel.resources import Locale, Provider
from jobfunnel.resources.defaults import (
    DEFAULT_SEARCH_RADIUS_KM, DEFAULT_MAX_LISTING_DAYS,
    DEFAULT_DOMAIN_FROM_LOCALE,
)

class SearchConfig(BaseConfig):
    """Config object to contain region of interest for a Locale

    FIXME: ideally we'd have one of these per-locale, per-website, but then
    the config would be a nightmare, so we'll just put everything in here
    for now
    """

    def __init__(self,
                 keywords: List[str],
                 province_or_state: Optional[str],
                 locale: Locale,
                 providers: List[Provider],
                 city: Optional[str] = None,
                 distance_radius: Optional[int] = None,
                 return_similar_results: Optional[bool] = False,
                 max_listing_days: Optional[int] = None,
                 blocked_company_names: Optional[List[str]] = None,
                 domain: Optional[str] = None):
        """Search config for all job sources

        Args:
            keywords (List[str]): list of search keywords
            province_or_state (str): province or state.
            city (Optional[str], optional): city. Defaults to None.
            distance_radius (Optional[int], optional): km/m radius. Defaults to
                DEFAULT_SEARCH_RADIUS_KM.
            return_similar_results (Optional[bool], optional): return similar.
                results (indeed), Defaults to False.
            max_listing_days (Optional[int], optional): oldest listing to show.
                Defaults to DEFAULT_MAX_LISTING_DAYS.
            blocked_company_names (Optional[List[str]]): list of names of
                companies that we never want to see in our results.
            domain (Optional[str], optional): domain string to use for search
                querying. If not passed, will set based on locale. (i.e. 'ca')
        """
        self.province = province_or_state
        self.state = province_or_state
        self.city = city.lower()
        self.radius = distance_radius or DEFAULT_SEARCH_RADIUS_KM
        self.locale = locale
        self.providers = providers
        self.keywords = keywords
        self.return_similar_results = return_similar_results  # indeed thing
        self.max_listing_days = max_listing_days or DEFAULT_MAX_LISTING_DAYS
        self.blocked_company_names = blocked_company_names

        self.__query_string = '' # type: str

        # Try to infer the domain string based on the locale.
        if not domain:
            if not self.locale in DEFAULT_DOMAIN_FROM_LOCALE:
                raise ValueError(f"Unknown domain for locale: {self.locale}")
            self.domain = DEFAULT_DOMAIN_FROM_LOCALE[self.locale]
        else:
            self.domain = domain

    @property
    def query_string(self) -> str:
        """User-readable version of the keywords we are searching with
        """
        if not self.__query_string:
            self.__query_string = ' '.join(self.keywords)
        return self.__query_string

    def validate(self):
        """We need to have the right information set, not mixing stuff
        FIXME: impl.
        """
        pass
