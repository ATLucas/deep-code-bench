# OpenAI Agents
from agents import Agent, ModelSettings, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
from openai.types.shared.reasoning import Reasoning


async def run_agent(project_dir: str, workflow_name: str):
    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", project_dir],
        },
        cache_tools_list=True,
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name=workflow_name, trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n"
            )
            await _run_agent(server, project_dir)


async def _run_agent(mcp_server: MCPServer, project_dir: str):
    agent = Agent(
        name="File Assistant",
        instructions=f"""Use the tools to read the filesystem and answer questions based on those files.
        You only have access to the following directory: {project_dir}.""",
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
