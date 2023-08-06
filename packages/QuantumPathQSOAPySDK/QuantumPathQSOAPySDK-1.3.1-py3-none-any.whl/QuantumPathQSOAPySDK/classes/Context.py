from .apiConnection import apiConnection

class Context:

    # CONSTRUCTOR
    def __init__(self, username: str, password: str, url: str):
        self.__credentials = {
            "Username": username,
            "Password": password
        }

        self.__authToken = apiConnection(url, self.__credentials, 'string', 'data')

        self.__header = {
            "Authorization": 'Bearer ' + str(self.__authToken)
        }


    # GETTERS
    def getCredentials(self) -> dict:
        return self.__credentials

    def getAuthToken(self) -> str:
        return self.__authToken
    
    def getHeader(self) -> dict:
        return self.__header