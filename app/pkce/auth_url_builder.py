class URLBuilder:
    """
    A utility class for building URLs with query parameters.

    This class allows users to build URLs with query parameters by providing a base URL and adding query parameters using the add_query_param method. The create method can then be called to generate the full URL with all the added query parameters.

    Attributes:
    base_url (str): The base URL to which query parameters will be added.
    query_params (dict): A dictionary of query parameters and their values.

    Methods:
    add_query_param(param: str, value: str) -> None: Add a query parameter to the URL.
    create() -> str: Create the full URL with all added query parameters.
    """
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.query_params = {}
    
    def add_query_param(self, param: str, value: str) -> None:
        self.query_params[param] = value
    
    def create(self) -> str:
        url = self.base_url + "?"
        for param, value in self.query_params.items():
            url += f"{param}={value}&"
        return url[:-1]  # Remove the trailing "&"
