class CompaniesHouseAPI:

    import logging
    import base64
    import requests
    from typing import Optional, Dict, Any
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    # from .Config import Config
    # from .RateLimiter import RateLimiter
    # from .APIResponse import APIResponse
    # from COMPANIES-HOUSE-PROJECT.python_examples.Fix_Pydantic_nested_models \
    #     import Config, APIResponse, RegisteredOffice, CompanyData
    # import Fix_Pydantic_nested_models
    from chtools.Company_Info import Config, APIResponse, RegisteredOffice, CompanyData
    from chtools.RateLimiter import RateLimiter
    from chtools.get_api_key import get_api_key
    from chtools.setup_logging import setup_logging
    logger = setup_logging()
    api_key = get_api_key()

    """Handler for Companies House API interactions."""

    def __init__(self, api_key: str, logger: logging.Logger, rate_limiter: Optional[RateLimiter] = None, config: Optional[Config] = None):
        self.api_key = api_key
        self.logger = logger
        # Pass logger to RateLimiter
        self.rate_limiter = rate_limiter or RateLimiter(config.MAX_REQUESTS, config.TIME_WINDOW, self.logger)  # If rate limiter not passed in use a default one
        self.session = self._create_session()
        self.config = config if config else Config(api_key=api_key)

        # Create base64 encoded authentication
        auth = base64.b64encode(f"{api_key}:".encode('ascii')).decode('ascii')
        self.headers = {
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json'
        }
        self.logger.debug("CompaniesHouseAPI Initialized")

    @staticmethod
    def _create_session() -> requests.Session:
        """Create a session with retry strategy."""
        
        import requests
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry

        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    def search_companies(self, search_term: str, start_index: int = 0) -> Optional[APIResponse]:
        """Search for companies using the Companies House API."""
        params = {
            'q': search_term,
            'items_per_page': self.config.ITEMS_PER_PAGE,
            'start_index': start_index,
            'company_status': 'active'
        }

        try:
            self.rate_limiter.wait_if_needed()

            if start_index >= self.config.MAX_RESULTS:
                self.logger.info(f"Reached maximum results limit ({self.config.MAX_RESULTS}) for search term: {search_term}")
                return APIResponse(items=[])

            response = self.session.get(
                f"{self.config.BASE_URL}/search/companies",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            return APIResponse(**response.json())

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request: {e}")
            return None

    def get_company_details(self, company_number: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific company."""
        try:
            self.rate_limiter.wait_if_needed()

            response = self.session.get(
                f"{self.config.BASE_URL}/company/{company_number}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching details for company {company_number}: {e}")
            return None