"""
Understanding the problem
Imagine you're building a FastAPI backend for an AI assistant.
A client sends the following request:
request = {    "user_id": "user_101",    "prompt": "Explain transformer architecture",    "temperature": 0.7,    "max_tokens": 512}


Before passing this request to an LLM, your application must validate its contents.
What happens if the client sends a negative max_tokens value, an empty prompt, or an invalid temperature?
Without validation, malformed requests can reach expensive downstream services and cause avoidable failures.
Your task is to implement a reusable Python request validator.
Required interface
class RequestValidationError(ValueError):   
      Raised when an AI request contains invalid data.\"""def validate_ai_request(request: dict) -> dict:    \"""    Validate and normalize an incoming AI request.    Return a new dictionary containing validated values.    Raise RequestValidationError for invalid requests.    Never mutate the original request.    \"""    
pass


Validation requirements

Your validator must enforce the following contract.

Field	Requirement

user_id	Required, nonempty string
prompt	Required string, 1–2,000 characters after trimming
temperature	Optional finite number between 0 and 2; default 0.7
max_tokens	Optional integer between 1 and 4,096; default 512


Whitespace-only user_id and prompt values must be rejected. Boolean values must not be accepted as numeric values, even though Python treats bool as a subclass of int.
Reject unknown fields rather than silently accepting them. Return a new dictionary containing the validated values, including defaults.

"""

#valid helpers 


    
class RequestValidationError(ValueError):
    """Raised when an AI request contains invalid data."""

    
def _validate_string( 
        value : str ,field : str, min_len : int = 1 , max_len : int = None 
) : 
    if not isinstance(value,str) :
        raise RequestValidationError(f"{field} must be a string")
    if not value.strip() :
        raise RequestValidationError(f"{field} must be a nonempty string")
    if len(value) < min_len :
        raise RequestValidationError(f"{field} must be at least {min_len} characters")
    if max_len and len(value) > max_len :
        raise RequestValidationError(f"{field} must be at most {max_len} characters")

def _validate_int( 
        value : int ,field : str , min_val : int = 1, max_val : int = 4096 ,default : int = 512
) : 
    if not isinstance(value,int):
        raise RequestValidationError(f"{field} must be an integer")
    if not min_val <= value <= max_val :
        raise RequestValidationError(f"{field} must be between {min_val} and {max_val}")
    return value

def _validate_number(
        value : int , field : str , min_val : float = 0, max_val : float = 2, default : float = 0.7
) : 
    if not isinstance(value, (int, float)) :
        raise RequestValidationError(f"{field} must be a number")
    if not min_val <= value <= max_val :
        raise RequestValidationError(f"{field} must be between {min_val} and {max_val}")
    return value


def validate_ai_request(request: dict) -> dict:
    if not isinstance(request, dict):
        raise RequestValidationError("Request must be a dictionary")

    allowed_fields = {"user_id", "prompt", "temperature", "max_tokens"}
    unknown_fields = set(request.keys()) - allowed_fields
    if unknown_fields:
        raise RequestValidationError(f"Unknown fields: {', '.join(unknown_fields)}")

    validated = {}

    # user_id
    if "user_id" not in request:
        raise RequestValidationError("Missing required field: user_id")
    validated["user_id"] = _validate_string(request["user_id"], "user_id")

    # prompt
    if "prompt" not in request:
        raise RequestValidationError("Missing required field: prompt")
    validated["prompt"] = _validate_string(request["prompt"], "prompt", 1, 2000)
    print(f"Validated prompt: {validated['prompt']}")

    # temperature
    validated["temperature"] = _validate_number(
        request.get("temperature"), "temperature", 0.0, 2.0, 0.7
    )
    print(f"Temperature {validated['temperature']}")
    # max_tokens
    validated["max_tokens"] = _validate_int(
        request.get("max_tokens"), "max_tokens", 1, 4096, 512
    )
    print(f"Max tokens: {validated['max_tokens']}")

    return validated

request = {
    "user_id": "user_101",
    "prompt": "Explain transformer architecture",
    "temperature": 0.7,
    "max_tokens": 512,
}

try:
    valid = validate_ai_request(request)
    print("Validated request:", valid)
except RequestValidationError as e:
    print("Validation failed:", e)
