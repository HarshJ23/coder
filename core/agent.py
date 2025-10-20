import json
import os
from exa_py import Exa
from litellm import completion
from dotenv import load_dotenv
from tools.tool_directory import tools , available_functions
from typing import Any



load_dotenv()

groq_api_key  = os.getenv("groq_api_key")

os.environ['GROQ_API_KEY'] = groq_api_key



tot_completion_token = 0
tot_prompt_tokens = 0
tot_tokens = 0


def calc_tokens(completion_tokens , prompt_tokens , total_tokens):
    global tot_completion_token , tot_prompt_tokens , tot_tokens
    tot_completion_token += completion_tokens
    tot_prompt_tokens += prompt_tokens
    tot_tokens += total_tokens

# Agent class - system prompt , tools , conversation state , model
# model = "groq/moonshotai/kimi-k2-instruct-0905"





class Coder:
    def __init__(self, name,  system_prompt, model, agent_tools):
        self.name = name
        self.messages = [{"role": "system", "content": system_prompt}]
        self.llm_model = model
        self.agent_tools = agent_tools
        self.token_usage = {"completion": 0, "prompt": 0, "total": 0}

    def update_tokens(self, usage):
        """Update and display per-session token counters."""
        self.token_usage["completion"] += usage.completion_tokens
        self.token_usage["prompt"] += usage.prompt_tokens
        self.token_usage["total"] += usage.total_tokens

    def run(self, user_query: str) -> Any:
        """Run the agent loop, yielding structured events instead of printing."""
        self.messages.append({"role": "user", "content": user_query})

        while True:
            response = completion(
                model=self.llm_model,
                messages=self.messages,
                tools=self.agent_tools,
                tool_choice="auto",
            )

            # token usage
            if hasattr(response, "usage"):
                self.update_tokens(response.usage)
                yield {
                    "type": "usage",
                    "data": {
                        "prompt": response.usage.prompt_tokens,
                        "completion": response.usage.completion_tokens,
                        "total": response.usage.total_tokens,
                    },
                }

            response_message = response.choices[0].message
            tool_calls = getattr(response_message, "tool_calls", None)

            # yield LLM response
            if response_message.content:
                yield {
                    "type": "llm_response",
                    "data": {"content": response_message.content.strip()},
                }

            # if no tool calls, final answer
            if not tool_calls:
                yield {
                    "type": "final_content",
                    "data": {"content": response_message.content},
                }
                break

            self.messages.append(response_message)

            # handle tool calls
            for tool_call in tool_calls:
                yield {
                    "type": "tool_call",
                    "data": {
                        "tool_name": tool_call.function.name,
                        "tool_arguments": json.loads(
                            tool_call.function.arguments
                        ),
                    },
                }

                fname = tool_call.function.name
                fargs = json.loads(tool_call.function.arguments)

                if fname not in available_functions:
                    yield {
                        "type": "error",
                        "data": {"message": f"Tool {fname} not implemented."},
                    }
                    continue

                f = available_functions[fname]

                try:
                    fresp = f(**fargs)
                except Exception as e:
                    fresp = type('MockResponse', (), {'data': f"Tool call failed: {str(e)}"})()
                    yield {
                    "type": "error",
                    "data": {
                        "message": f"{fname} tool call failed",
                            "details": str(e),
                        },
                    }

                # yield tool response
                yield {
                    "type": "tool_response",
                    "data": {"tool_name": fname, "content": fresp.data},
                }

                # append tool response into conversation
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": fname,
                        "content": json.dumps(fresp.data),
                    }
                )
        print(self.messages)


