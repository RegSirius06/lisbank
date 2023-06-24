# PATCH that fix a Python Bug:
import sys
import asyncio

if sys.platform == "win32" and sys.version_info >= (3, 11, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())