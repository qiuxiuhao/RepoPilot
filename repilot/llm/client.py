from openai import OpenAI
import os
from repilot.config import LLMConfig
from repilot.llm.schemas import LLMRequest,LLMResponse,TokenUsage

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
        response = self.client.responses.create(
            model = self.config.model,
            instructions = request.instructions,
            input = request.user_input,
            reasoning = {
                "effort": self.config.reasoning_effort
            },
            max_output_tokens = self.config.max_output_tokens,
        )
        #print(response)

        usage = None

        if response.usage is not None:
            usage = TokenUsage(
                input_tokens =response.usage.input_tokens,
                output_tokens = response.usage.output_tokens,
                total_tokens = response.usage.total_tokens,
            )

        return LLMResponse(
           text = response.output_text,
           model=response.model,
           response_id = response.id,
           usage=usage, 
        )