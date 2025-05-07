import asyncio
from async_python.chapter_2.Blocking_apis import main as main_blocking_apis
from async_python.chapter_2.debug_mode import main as main_debug_mode

asyncio.run(main_debug_mode())
