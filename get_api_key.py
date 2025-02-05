def get_api_key() -> str:

    import getpass
    
    MAX_ATTEMPTS = 3        # set the maximum number of attempts
    attempts = 0
    
    while attempts < MAX_ATTEMPTS:
        key = getpass.getpass(f"Enter Companies House API key (attempt {attempts + 1}/{MAX_ATTEMPTS}): ")
        
        class SecureString:
            def __init__(self, value): 
                self._value = value
                self._is_valid = len(value) == 36
                
            def __str__(self):
                if self._is_valid:
                    return "****API KEY****"
                return f"Invalid api_key: {self._value}"
                
            def __repr__(self):
                return self.__str__()
                
            def get(self):
                return self._value
            
            def is_valid(self):
                return self._is_valid

        secure_key = SecureString(key)
        if secure_key.is_valid():
            return secure_key
            
        print(secure_key)  # This will print the invalid key message
        attempts += 1
        
    raise ValueError("Failed to provide valid API key after 3 attempts")

if __name__ == "__main__":
    try:
        api_live_key = get_api_key()
        print(api_live_key)
    except ValueError as e:
        print(e)