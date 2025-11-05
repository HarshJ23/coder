from .agent import Coder
from .tools.tool_directory import tools , available_functions 


class SubCoder:
    # no init -- factory patter -- will instantiate another class

    @staticmethod
    def create_subagent(name : str  , description : str , task : str , tools_list):
        # here , tools will be a list of tool names need to be given to this subagent 
        # sub_agent_tools  = []
        #  ex : ["web_search_tool" , "read_file_tool"]
        #  for tool in tools_list:
        #       for tl in tools:
        #           if tool == tl["function"]["name"]
        #           sub_agent_tools.append(tl)
        sub_agent_tools  = []
        for tool in tools_list:
            for tl in tools:
                if tool == tl["function"]["name"]:
                    sub_agent_tools.append(tl)

        sub_sys_prompt = description + task    
        sub_coder =  Coder(name = name , system_prompt=sub_sys_prompt , model = "groq/moonshotai/kimi-k2-instruct-0905"  , agent_tools=sub_agent_tools)        
        return sub_coder

        # return sub_agent_tools
        # pass



# testing -----
# tools_list = ["web_search_tool" , "read_file_tool"]
# res = SubCoder.create_subagent("sub_agent_1" , "sub_agent_1" , "sub_agent_1" , tools_list)
# print(res)