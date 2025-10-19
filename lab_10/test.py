import asyncio

async def print_something(test):
    while True:
        print(test)
        await asyncio.sleep(1)
    
async def insert_something():
    while True:
        print("insert")
        await asyncio.sleep(3)


async def main():
    task_1 = asyncio.create_task(print_something("smth"))
    task_2 = asyncio.create_task(insert_something())
    await asyncio.gather(task_1, task_2)

if __name__ == "__main__":
    asyncio.run(main())
