# IGNORE - not used


import json
import re

# Paste your list here (e.g. `data = [...]`)
data = [ ... ]  # your raw conversation list

def parse_agent_log(raw):
    parsed = []
    for item in raw:
        entry = {}

        # Handle dicts or Message objects
        if isinstance(item, dict):
            entry['role'] = item.get('role')
            entry['content'] = item.get('content', '')
            if 'name' in item:
                entry['name'] = item['name']
        elif hasattr(item, '__dict__'):  # if it's a Message object
            entry.update(item.__dict__)
        else:
            continue

        # Parse Playwright-like tool calls if present
        tools = []
        if 'tool_calls' in entry and entry['tool_calls']:
            for t in entry['tool_calls']:
                tool_info = {
                    "name": t.get("function", {}).get("name"),
                    "arguments": t.get("function", {}).get("arguments"),
                    "id": t.get("id")
                }
                tools.append(tool_info)
        entry['tools_used'] = tools

        # If the tool returned content (like JSON output), parse it
        if entry.get('role') == 'tool' and entry.get('content'):
            try:
                content_json = json.loads(entry['content'])
                entry.update(content_json)
            except json.JSONDecodeError:
                entry['output'] = entry['content']

        parsed.append(entry)

    return parsed

parsed_log = parse_agent_log(data)

# Pretty-print it
print(json.dumps(parsed_log, indent=2))

