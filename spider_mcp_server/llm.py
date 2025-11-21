from operator import ge
from enum import Enum
from crawl4ai import LLMConfig, LLMExtractionStrategy, CrawlerRunConfig, CacheMode
from pydantic import BaseModel
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

import os
import litellm

from spider_mcp_server.config import OLLAMA_API_BASE, OLLAMA_MODEL, OLLAMA_TOKEN, OLLAMA_MAX_INPUT_LEN


DEFAULT_INSTRUCTION = """
提取此页面的主要文章内容，包括标题和段落。以JSON格式输出，并包含在一个'content'字段中。
"""

def llm_config(
    instruction: str = DEFAULT_INSTRUCTION,
    save_screenshot: bool = False,
    save_pdf: bool = False,
    generate_markdown: bool = False
):
    litellm.client_session_timeout = 3000
    # litellm._turn_on_debug() 
    
    print(f"LLM instruction: \n{instruction}")

    # LLM extraction strategy
    llm_strat = LLMExtractionStrategy(
        llm_config = LLMConfig(
                provider=OLLAMA_MODEL,
                api_token=OLLAMA_TOKEN,
                base_url=OLLAMA_API_BASE,
                max_tokens=OLLAMA_MAX_INPUT_LEN
            ),
        input_format="html",
        extraction_type="schema",
        instruction=instruction,
        apply_chunking=True,
        force_json_response=True,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        verbose=True,
        extra_args={"temperature": 0.0, "max_tokens": 800}
    )
    
    llm_strat.show_usage()
    llm_strat.verbose = True

    markdown_gen = DefaultMarkdownGenerator() if generate_markdown else None

    # type: ignore
    return CrawlerRunConfig(
        extraction_strategy=llm_strat,
        screenshot=save_screenshot,
        pdf=save_pdf,
        markdown_generator=markdown_gen,
        cache_mode=CacheMode.DISABLED,
        word_count_threshold=1,
        remove_overlay_elements=True,
        only_text=False 
    )