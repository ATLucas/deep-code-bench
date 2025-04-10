# Standard
import os

# OpenAI Agents
from agents import Agent, ModelSettings, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
from openai.types.shared.reasoning import Reasoning

# DCB
from dcb.init.init_test import init_test


async def run_test(work_dir: str, test_name: str, checkpoint_dir: str = None):
    test_dir = await init_test(work_dir, test_name, checkpoint_dir)

    # async with MCPServerStdio(
    #     name="Filesystem Server, via npx",
    #     params={
    #         "command": "npx",
    #         "args": ["-y", "@modelcontextprotocol/server-filesystem", test_dir],
    #     },
    #     cache_tools_list=True,
    # ) as server:
    #     trace_id = gen_trace_id()
    #     with trace(workflow_name=f"DC Benchmark Test {test_name}", trace_id=trace_id):
    #         print(
    #             f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n"
    #         )
    #         await run_test_inner(server, test_dir)


async def run_test_inner(mcp_server: MCPServer, test_dir: str):
    agent = Agent(
        name="File Assistant",
        instructions=f"""Use the tools to read the filesystem and answer questions based on those files.
        You only have access to the following directory: {test_dir}.""",
        model="o3-mini",
        model_settings=ModelSettings(
            reasoning=Reasoning(
                effort="low",  # low, medium, high
            ),
        ),
        mcp_servers=[mcp_server],
    )

    result = None

    while True:
        message = input("\nEnter your query (or 'exit' to quit): ").strip()

        if message.lower() == "exit":
            print("Exiting benchmark test...")
            break

        if not message:  # Skip empty inputs
            continue

        if result:
            new_input = result.to_input_list() + [{"role": "user", "content": message}]
        else:
            new_input = [{"role": "user", "content": message}]

        result = await Runner.run(starting_agent=agent, input=new_input)
        print("\nResponse:", result.final_output)
