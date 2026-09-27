from dataclasses import dataclass
from pathlib import Path

import yaml

@dataclass
class LLMConfig:
    provider:str
    model:str
    base_url:str
    reasoning_effort:str
    max_output_tokens:int

@dataclass
class AppConfig:
    llm:LLMConfig

def load_config(path:str | Path = "config.yaml")->AppConfig:
    path = Path(path)

    with path.open("r",encoding="utf-8") as file:
        raw_config = yaml.safe_load(file)

    llm_config = LLMConfig(
        provider=raw_config["llm"]["provider"],
        model=raw_config["llm"]["model"],
        base_url=raw_config["llm"]["base_url"],
        reasoning_effort=raw_config["llm"]["reasoning_effort"],
        max_output_tokens=raw_config["llm"]["max_output_tokens"],
    )
    return AppConfig(llm=llm_config)