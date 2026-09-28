from openai import OpenAI
import os,json
from repilot.config import LLMConfig
from repilot.llm.schemas import (
    LLMRequest,
    LLMResponse,
    TokenUsage,
    ToolCall
)
from typing import Any

class LLMClient:
    def __init__(self,config:LLMConfig):
        self.config =  config

        api_key = os.environ.get("DEEPSEEK_API_KEY")

        if not api_key:
            raise RuntimeError( "DEEPSEEK_API_KEY is not set.")

        self.client = OpenAI(
            api_key = api_key,
            base_url = self.config.base_url, 
        )

    def generate(self,request:LLMRequest)->LLMResponse:
        request_args:dict[str,Any] = { 
            "model": self.config.model,
            "instructions":request.instructions,
            "input":request.user_input,
            "reasoning":{
                "effort":(self.config.reasoning_effort)
            },
            "max_output_tokens":(self.config.max_output_tokens),
            }
        
        if request.tools:
            request_args["tools"] = request.tools
            request_args["tool_choice"]=(request.tool_choice)

        response = self.client.responses.create(**request_args)

        usage = None

        if response.usage is not None:
            usage = TokenUsage(
                input_tokens =response.usage.input_tokens,
                output_tokens = response.usage.output_tokens,
                total_tokens = response.usage.total_tokens,
            )

        tool_calls:list[ToolCall] = []

        for item in response.output:
            if item.type != "function_call":
                continue
            
            raw_arguments = item.arguments

            try:
                arguments = json.loads(raw_arguments)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Model returned invalid JSON "
                    f"arguments for tool "
                    f"{item.name}: "
                    f"{raw_arguments}"
                ) from exc

            if not isinstance(arguments,dict):
                 raise ValueError(
                    "Tool arguments must decode "
                    "to a JSON object."
                )

            tool_calls.append(ToolCall(call_id=item.call_id,
                name=item.name,arguments=arguments,raw_arguments=raw_arguments))

        return LLMResponse(
           text = response.output_text,
           model=response.model,
           response_id = response.id,
           usage=usage, 
           tool_calls=tool_calls,
        )