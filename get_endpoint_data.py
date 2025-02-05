from typing import Optional, Dict, Any
from chtools.CompaniesHouseAPI import CompaniesHouseAPI
from chtools.Company_Info import APIResponse

def get_endpoint_data(
    api: CompaniesHouseAPI,
    endpoint: str,
    params: Optional[Dict[str, str]] = None,
    **kwargs
) -> Optional[APIResponse]:
    """
    Fetches data from the Companies House API for a given endpoint.

    Parameters:
        api: An instance of the CompaniesHouseAPI class.
        endpoint: The endpoint to fetch.
        params: A dictionary of query parameters for the request.
        kwargs: Extra keyword arguments for the requests.get method.
    Returns:
         An APIResponse object containing the response items and results.
    Raises:
        HTTPError: If the request returns an HTTP error status code.
    """
    try:
        response = api.request_with_rate_limit(endpoint=endpoint, params=params, **kwargs)

        if response.is_ok():
            return APIResponse(**response.data)
        else:
             api.logger.error(f"API request failed with status code {response.status_code}: {response.error}")
             return None
    except Exception as e:
         api.logger.error(f"Unexpected error: {e}")
         return None