import asyncio

a = [0,]*15
b = [0,]*10

async def update(lst, i):
    await asyncio.sleep(i)
    lst[i] = i
    print(i)
    return i


async def main():
    lst = await asyncio.gather(*(
                asyncio.create_task(update(a, i)) for i in range(15)
            ), *(
                asyncio.create_task(update(b, i)) for i in range(10)
            ))
    #print(a,b)
    print(lst)


if __name__ == "__main__":
    asyncio.run(main())
