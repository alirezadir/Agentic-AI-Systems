## Modern Python for Gen-AI
- **Modern Python**
    - **asyncio**: asynchronous I/O (`async`, `async.run()`, `await`)
        - `async`: define an async function
        - `asyncio.run()`: run an async function
        - `await`: wait for an async function to complete w/o blocking the main thread; 
            - `await` only used inside an `async def` function
        ```python
        import asyncio
        async def main():
            await asyncio.sleep(1)
            print("Hello, async world!")
        asyncio.run(main())
        # Hello, async world!
        ```
        - `asyncio.gather()`: run multiple async functions in parallel
    - **Docstrings**: documentation strings for Python functions and classes ("""...""")
    - **OOP** concepts used often (inheritance, metaclasses, decorators (e.g. `@dataclass, @property, @tool`)), etc.
    - `pydantic`: data validation, parsing, and serialization management using Python type annotations
        - type enforcement, auto conversion, and serialization(`.dict(), .json()`)
- **Containers**: Docker (build, run, push; Dockerfile)
- **Package managers**:
    - [Python uv](https://www.datacamp.com/tutorial/python-uv): new, ultra-fast Python package manager; recommended for GenAI
        `$ brew install uv`
        `$ uv init explore-uv`
        `$ uv add llama-index`
- **Vibe Coding / Chat-Oriented Programming (CHOP)**
    - [Cursor](https://www.cursor.com/en/features)
    - Microsoft Copilot 
- **UI**
    - [Gradio](https://gradio.app/)
    - [Streamlit](https://streamlit.io/)
        - [streamlit-magic](https://docs.streamlit.io/library/api-reference/write-magic/magic)
        - [LLM chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
        - [streamlit-gpt4](https://blog.streamlit.io/take-your-streamlit-apps-to-the-next-level-with-gpt-4/)
- [Python 3 Cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)