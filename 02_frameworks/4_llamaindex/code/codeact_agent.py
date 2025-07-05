"""
LlamaIndex CodeAct Agent — From Scratch Example

This script demonstrates how to build a CodeAct Agent from scratch, including:
- Math function tools
- A simple code executor with state persistence
- A custom agent workflow

Reference:
    https://docs.llamaindex.ai/en/stable/examples/agent/from_scratch_code_act_agent/
"""

import io
import contextlib
import ast
import traceback
import inspect
import re
from typing import Any, Dict, Tuple

from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_index.core.workflow import (
    Workflow, step, StartEvent, StopEvent, Event, Context
)

# ----------------------------------------------------------------------
# Math helper functions for the agent

def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    return a / b

# ----------------------------------------------------------------------
# Simple code executor with state persistence

class SimpleCodeExecutor:
    """
    A simple code executor that runs Python code with state persistence.
    Not safe for production use! Use with caution.
    """
    def __init__(self, locals: Dict[str, Any] = None, globals: Dict[str, Any] = None):
        self.globals = globals or {}
        self.locals = locals or {}

    def execute(self, code: str) -> Tuple[bool, str, Any]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        output = ""
        return_value = None
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:
                    tree = ast.parse(code)
                    last_node = tree.body[-1] if tree.body else None
                    if isinstance(last_node, ast.Expr):
                        last_line = code.rstrip().split("\n")[-1]
                        exec_code = code[: -len(last_line)] + "\n__result__ = " + last_line
                        exec(exec_code, self.globals, self.locals)
                        return_value = self.locals.get("__result__")
                    else:
                        exec(code, self.globals, self.locals)
                except Exception:
                    exec(code, self.globals, self.locals)
            output = stdout.getvalue()
            if stderr.getvalue():
                output += "\n" + stderr.getvalue()
        except Exception as e:
            output = f"Error: {type(e).__name__}: {str(e)}\n"
            output += traceback.format_exc()
            return False, output, None
        return True, output, return_value

# ----------------------------------------------------------------------
# CodeActAgent definition (custom workflow)

CODEACT_SYSTEM_PROMPT = (
    "You are a helpful code assistant.\n\n"
    "You can use the following functions:\n\n"
    "{fn_str}\n\n"
    "When you want to execute code, wrap it in <execute>...</execute> tags.\n"
)

class CodeExecutionEvent(Event):
    code: str

class StreamEvent(Event):
    delta: str

class InputEvent(StartEvent):
    input: list

class CodeActAgent(Workflow):
    def __init__(self, fns, code_execute_fn, llm):
        super().__init__()
        self.fns = fns
        self.code_execute_fn = code_execute_fn
        self.llm = llm
        # Build function signatures for system prompt
        self.fn_str = "\n\n".join(
            f'def {fn.__name__}{str(inspect.signature(fn))}:\n    """{fn.__doc__}"""\n    ...'
            for fn in self.fns
        )
        self.system_message = ChatMessage(
            role="system",
            content=CODEACT_SYSTEM_PROMPT.format(fn_str=self.fn_str),
        )

    def _parse_code(self, response: str) -> str | None:
        matches = re.findall(r"<execute>(.*?)</execute>", response, re.DOTALL)
        if matches:
            return "\n\n".join(matches)
        return None

    @step
    async def prepare_chat_history(self, ctx: Context, ev: StartEvent) -> InputEvent:
        memory = await ctx.store.get("memory", default=None)
        if not memory:
            memory = ChatMemoryBuffer.from_defaults(llm=self.llm)
        user_input = ev.get("user_input")
        if user_input is None:
            raise ValueError("user_input kwarg is required")
        user_msg = ChatMessage(role="user", content=user_input)
        memory.put(user_msg)
        chat_history = memory.get()
        await ctx.store.set("memory", memory)
        return InputEvent(input=[self.system_message, *chat_history])

    @step
    async def handle_llm_input(self, ctx: Context, ev: InputEvent) -> CodeExecutionEvent | StopEvent:
        chat_history = ev.input
        response_stream = await self.llm.astream_chat(chat_history)
        full_response = ""
        async for response in response_stream:
            full_response += response.delta or ""
            ctx.write_event_to_stream(StreamEvent(delta=response.delta or ""))
        memory = await ctx.store.get("memory")
        memory.put(ChatMessage(role="assistant", content=full_response))
        await ctx.store.set("memory", memory)
        code = self._parse_code(full_response)
        if not code:
            return StopEvent(result=full_response)
        else:
            return CodeExecutionEvent(code=code)

    @step
    async def handle_code_execution(self, ctx: Context, ev: CodeExecutionEvent) -> InputEvent:
        ctx.write_event_to_stream(ev)
        success, output, return_value = self.code_execute_fn(ev.code)
        memory = await ctx.store.get("memory")
        memory.put(ChatMessage(role="assistant", content=str(output)))
        await ctx.store.set("memory", memory)
        chat_history = memory.get()
        return InputEvent(input=[self.system_message, *chat_history])

# ----------------------------------------------------------------------
# Example usage: running the agent on math/code queries

import asyncio

def main():
    # Instantiate code executor and agent
    code_executor = SimpleCodeExecutor(
        locals={},
        globals={
            "add": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide,
        }
    )
    llm = OpenAI(model="gpt-4o-mini", api_key="sk-...")
    agent = CodeActAgent(
        fns=[add, subtract, multiply, divide],
        code_execute_fn=code_executor.execute,
        llm=llm,
    )
    ctx = Context(agent)

    async def run_agent_verbose(agent, ctx, query):
        handler = agent.run(user_input=query, ctx=ctx)
        print(f"User:  {query}")
        async for event in handler.stream_events():
            if isinstance(event, StreamEvent):
                print(f"{event.delta}", end="", flush=True)
            elif isinstance(event, CodeExecutionEvent):
                print(f"\n-----------\nParsed code:\n{event.code}\n")
        return await handler

    async def demo():
        await run_agent_verbose(agent, ctx, "Calculate the sum of all numbers from 1 to 10")
        await run_agent_verbose(agent, ctx, "Add 5 and 3, then multiply the result by 2")
        await run_agent_verbose(agent, ctx, "Calculate the sum of the first 10 fibonacci numbers")
        await run_agent_verbose(agent, ctx, "Calculate the sum of the first 20 fibonacci numbers")

    asyncio.run(demo())

if __name__ == "__main__":
    main()