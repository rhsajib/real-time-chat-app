

class UserCreationError(Exception):
    """Custom exception for user creation errors."""

    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(self.message)


"""
To send such a response from your FastAPI application, you can follow these steps:

1. Import the necessary modules:

```python
from fastapi import HTTPException
from pydantic import BaseModel
```

2. Define your validation error model using Pydantic. This model will represent the structure of the error messages you want to send to the client:

```python
class ValidationError(BaseModel):
    error: str
    errors: list[dict]
```

3. Create a function to raise a `HTTPException` with the desired status code and response body. In this case, you want to return a `422 Unprocessable Entity` status code with the error details:

```python
def validation_error_response(errors: list[dict]):
    raise HTTPException(
        status_code=422,
        detail=ValidationError(
            error="Validation Failed",
            errors=errors,
        ),
    )
```

4. When you need to send a validation error response, call this function and pass the error details as a list of dictionaries. Each dictionary should contain the `field` and `message` for a specific validation error.

Here's an example of how to use it in your FastAPI route:

```python
from fastapi import FastAPI, HTTPException, Depends, Form
from pydantic import BaseModel

app = FastAPI()

class ValidationError(BaseModel):
    error: str
    errors: list[dict]

def validation_error_response(errors: list[dict]):
    raise HTTPException(
        status_code=422,
        detail=ValidationError(
            error="Validation Failed",
            errors=errors,
        ),
    )

@app.post("/create-user")
async def create_user(email: str = Form(...), password: str = Form(...)):
    errors = []

    # Example validation checks
    if len(password) < 8:
        errors.append({"field": "password", "message": "Password must be at least 8 characters long"})

    # Perform other validation checks as needed

    if errors:
        validation_error_response(errors)

    # If validation passes, proceed to create the user
    # ...

    return {"message": "User created successfully"}
```

In this example, when the validation fails, the `validation_error_response` function is called, raising a `HTTPException` with the appropriate status code and response body. The client will receive a response similar to the one you provided:

```json
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "error": "Validation Failed",
  "errors": [
    {
      "field": "password",
      "message": "Password must be at least 8 characters long."
    }
  ]
}
```

You can customize the `validation_error_response` function and add more error checks based on your application's validation requirements.
"""
