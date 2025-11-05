from exa_py import Exa
import os
from dotenv import load_dotenv
from ..models.tool_models import ToolResponse

load_dotenv()


exa_api_key = os.getenv("exa_api_key")
exa_client = Exa(exa_api_key)


def web_search_tool(search_query: str) -> ToolResponse:
    """web search tool
    Args: search_query : str
    """
    try:
        result = exa_client.answer(search_query, text=True)
        print(f" Web Search Output: {result.answer}")
        # return f\"web search output stored at {mem_key} key. use read_memory_state tool to get the output\"
        return ToolResponse(
            status="success",
            data=result.answer,
            tool_name="web_search_tool"
        )
    except Exception as e:
        return ToolResponse(
            status="error",
            data=f"Search for {search_query} failed: {e}",
            tool_name="web_search_tool",
            error=f"Search for {search_query} failed: {e}"
        )


# test
# if __name__ == "__main__":
#     web_search_tool("give me latest info about statsig , exa and dia-atlassian deal.")
