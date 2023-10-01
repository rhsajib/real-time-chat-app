


class UserCreationError(Exception):
    """Custom exception for user creation errors."""

    def __init__(self, message="User creation failed"):
        self.message = message
        super().__init__(self.message)
