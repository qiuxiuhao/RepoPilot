from dataclasses import dataclass

@dataclass
class LLMRequest:
    user_input:str
    instructions:str | None = None

@dataclass
class TokenUsage:
    input_tokens:int
    output_tokens:int
    total_tokens:int

@dataclass
class LLMResponse:
    text:str
    model:str
    response_id:str
    usage:TokenUsage | None
