from lib.exception import CoreException


class Token:
    def __init__(self):
        self.values = []

    def push(self, username, token):
        if not isinstance(username, str):
            raise CoreException(f"invalid token username: '{username}'")
        if not token.isnumeric():
            raise CoreException(f"invalid token value: '{token}'")
        self.values.append([username, token])
        return

    def pop(self):
        if len(self.values) == 0:
            raise CoreException("can not pop token, no values")
        if len(self.values) == 1:
            return
        self.values.pop()
        return
    
    def get(self):
        if len(self.values) == 0:
            raise CoreException("can not get token, no values")
        return self.values[-1]
