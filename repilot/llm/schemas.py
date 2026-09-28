from dataclasses import dataclass,field
from typing import Any

@dataclass
class ToolCall:
    call_id:str
    name:str
    arguments:dict[str,Any]
    raw_arguments:str

@dataclass
class LLMRequest:
    user_input:str
    instructions:str | None = None
    tools:list[dict[str,Any]]| None = None
    tool_choice:str | dict[str,str] = "auto"

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
    tool_calls:list[ToolCall] = field(
        default_factory = list
    )
