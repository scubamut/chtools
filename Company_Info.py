#Pydantic  define `RegisteredOffice`, then call `CompanyData.model_rebuild()`.


# from pydantic import BaseModel, Field
# from typing import Optional, List
# from chtools import RegisteredOffice, CompanyData, APIResponse

# # Define the nested model first
# class RegisteredOffice(BaseModel):
#     address_line_1: Optional[str] = None
#     locality: Optional[str] = None
#     postal_code: Optional[str] = None
#     country: Optional[str] = None

# # Define the APIResponse model
# class APIResponse(BaseModel):
#     items: Optional[list] = None
#     total_results: Optional[int] = None
#     page_number: Optional[int] = None
#     kind: Optional[str] = 'None'

# # Then define CompanyData with the nested model
# class CompanyData(BaseModel):
#     registered_office: Optional[RegisteredOffice] = None
#     """Represents company data."""
#     company_number: str = Field(alias="company_number")
#     company_name: str = Field(alias="company_name")
#     company_status: str = Field(alias="company_status")
#     date_of_creation: str = Field(alias="date_of_creation")
#     registered_office_address: Optional["RegisteredOffice"] = Field(alias="registered_office_address") # nested model
#     sic_codes: List[str] = Field(default_factory=list, alias="sic_codes")
#     type: Optional[str] = Field(default=None, alias="type")
    
# if __name__ == "__main__":
#     # Now you can create instances
#     # company = CompanyData()
#     CompanyData.model_rebuild()
#     print(CompanyData())

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date

# Define the nested model first
class RegisteredOffice(BaseModel):

    address_line_1: Optional[str] = Field(default=None, alias="address_line_1")
    address_line_2: Optional[str] = Field(default=None, alias="address_line_2")
    postal_code: Optional[str] = Field(default=None, alias="postal_code")
    locality: Optional[str] = Field(default=None, alias="locality")
    region: Optional[str] = Field(default=None, alias="region")  
    country: Optional[str] = Field(default=None, alias="country")

# Define the APIResponse model
class APIResponse(BaseModel):
    """
    A Pydantic model to represent the response from the Companies House API.
    """
    items: List[Dict[str, Any]] = Field(default_factory=list, description="List of items in the API response.")
    total_results: Optional[int] = Field(default=None, description="Total number of results, if provided.")
    page_number: Optional[int] = Field(default=None, description="Page number of the results, if provided.")
    kind: Optional[str] = Field(default=None, description="Kind or type of the results, if provided.")

    def __repr__(self):
        return f"APIResponse(items={len(self.items) if self.items else 'None'}, total_results={self.total_results}, page_number={self.page_number}, kind='{self.kind}')"

    def __str__(self):
        return self.__repr__()

    def is_ok(self) -> bool:
        """
        Always returns true - The APIResponse object is simply a data transfer object, not a representation of an API response with success or failure.
         """
        return True

# Define CompanyData with all required fields as Optional
class CompanyData(BaseModel):
    company_number: Optional[str] = None
    company_name: Optional[str] = None
    company_status: Optional[str] = None
    date_of_creation: Optional[date] = None
    registered_office_address: Optional[RegisteredOffice] = None
    """Represents company data."""
    # company_number: str = Field(default=None, alias="company_number")
    # company_name: str = Field(default=None, alias="company_name")
    # company_status: str = Field(default=None, alias="company_status")
    # date_of_creation: str = Field(default=None, alias="date_of_creation")
    # registered_office_address: Optional["RegisteredOffice"] = Field(default=None, alias="registered_office_address") # nested model
    sic_codes: List[str] = Field(default_factory=list, alias="sic_codes")
    type: Optional[str] = Field(default=None, alias="type")

class Config:

    from pathlib import Path

    arbitrary_types_allowed = True


    def __init__(self, api_key):
        self.api_key = api_key    

    # API Settings
    BASE_URL = "https://api.companieshouse.gov.uk"
    MAX_RESULTS = 1000
    ITEMS_PER_PAGE = 100
    
    # Rate Limiting
    MAX_REQUESTS = 590
    TIME_WINDOW = 300  # seconds
    
    # SIC Codes for Insurance Companies
    INSURANCE_SIC_CODES = ['651', '652']
    
    # Search Terms
    SEARCH_TERMS = [
        "insurance company",
        "insurance limited",
        "insurance ltd",
        "insurance plc",
        "assurance company",
        "assurance limited",
        "assurance ltd",
        "assurance plc"
    ]
    
    # Output Directory
    OUTPUT_DIR = Path("insurance_companies_data")

if __name__ == "__main__":
    # Now you can create an empty instance
    company = CompanyData()
    print(company)
    
    # Or create with some data
    company_with_data = CompanyData(
        company_number="12345678",
        company_name="Test Company",
        company_status="active",
        date_of_creation=date(2020, 1, 1),
        registered_office_address=RegisteredOffice(
            address_line_1="123 Test St",
            locality="London",
            postal_code="SW1A 1AA",
            country="United Kingdom"
        )
    )
    print(company_with_data)
