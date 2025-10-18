from request_handler import RequestHandler

import asyncio


async def main():
    request_hander = RequestHandler()
    result = await request_hander.get_top_drivers_stats()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
