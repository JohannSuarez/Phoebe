class URLBuilder:
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
