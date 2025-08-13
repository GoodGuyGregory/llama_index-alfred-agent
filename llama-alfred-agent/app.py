import asyncio

import colorama
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from huggingface_hub import login
from dotenv import load_dotenv
import os

from tools import Tools

import random

from retriever import Retriever

partings = ['🎩 Tata for now sir.', 
            '🎩 Good day Master Wayne.', 
            '🎩 Enjoy yourself Master Wayne.',
            '🎩 Feel Free to summon me again for assistance.',
            '🎩 Always at your service sir.',
            ]

async def prompt_agent(agent_provider):
    
    while True:
        print(colorama.Fore.WHITE + "🎩 Ask me about a guest you've come across at the party sir, \n I'm here to help you...")
        prompt = input('🦇: ')
        print(colorama.Fore.WHITE + "-"*30)
        
        if prompt.lower() == "exit" or prompt.lower() == "quit":
            again = input(colorama.Fore.WHITE + "🎩 Will thank be all sir?\n🦇: ")
            
            if again.lower() == "yes" or again.lower() == "y":
                print(colorama.Fore.WHITE + "-"*30)
                break
        else:
            
            response = await agent_provider.run(prompt)
            print(f"🎩 Alfred's Response: {response}")
            print(colorama.Fore.WHITE + "-"*30)
        
    print(colorama.Fore.WHITE + f"👋 {partings[random.randint(0, len(partings))]}")
    print("-"*30)



async def main():
    load_dotenv()
    
    retriever = Retriever(confirm_load=True)
    print(colorama.Fore.WHITE + "-"*30)
    
    print(colorama.Fore.YELLOW + "Connecting Remote LLM 🛰️")
    
    HF_TOKEN = os.environ.get("HF_TOKEN")
    
    OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")
    
    AIRNOW_API_KEY = os.environ.get("AIRNOW_API_KEY")
    
    llm = HuggingFaceInferenceAPI(
        model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
        token=HF_TOKEN,
        provider='auto'
        )
    
    print(colorama.Fore.WHITE + "-"*30)
    
    print(colorama.Fore.YELLOW + "Initializing Agent's Tools... 🛠️")
    
    agent_tools = Tools(status_updates=True, weather_api_key=OPEN_WEATHER_API_KEY, air_now_api_key=AIRNOW_API_KEY).tool_belt
    
    found_tools = []
    
    found_tools.append(retriever.guest_info_tool)
    
    for tool in agent_tools:
        found_tools.append(tool)
        
    print(colorama.Fore.WHITE + "-"*30)
    
    print(colorama.Fore.YELLOW + "Creating Agent's Workflow...")
    
    
    alfred = AgentWorkflow.from_tools_or_functions(
        found_tools,
        llm=llm
    )
    
    print(colorama.Fore.GREEN + '👍 Agent built and Ready')
    print(colorama.Fore.WHITE + "-"*30)
    
    await prompt_agent(agent_provider=alfred)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("-"*30)
        print(colorama.Fore.WHITE + f"👋 {partings[random.randint(0, len(partings))]}")