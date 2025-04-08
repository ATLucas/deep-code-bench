import asyncio
import os
import shutil
import argparse

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="File Assistant",
        instructions="Use the tools to read the filesystem and answer questions based on those files.",
        model="o3-mini",
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

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run benchmark tests with specified working directory')
    parser.add_argument('-d', '--workdir', type=str, required=True,
                       help='Working directory containing benchmark tests')
    args = parser.parse_args()

    # Use the provided workdir instead of the hardcoded samples_dir
    workdir = os.path.abspath(args.workdir)
    if not os.path.exists(workdir):
        raise RuntimeError(f"Working directory '{workdir}' does not exist")

    # Count number of directories in the working directory
    dir_count = sum(1 for item in os.listdir(workdir) if os.path.isdir(os.path.join(workdir, item)))
    print(f"Found {dir_count} directories in {workdir}")

    # Create new benchmark test directory
    test_dir_name = f"bench_test_{dir_count}"
    test_dir_path = os.path.join(workdir, test_dir_name)
    os.makedirs(test_dir_path, exist_ok=True)
    print(f"Created benchmark test directory: {test_dir_path}")

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", test_dir_path],
        },
        cache_tools_list=True,
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name=f"DC Benchmark Test {dir_count}", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    asyncio.run(main())