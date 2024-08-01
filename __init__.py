'''

pip install -e .

'''


import asyncio

async def counter(name: str):
    for i in range(0, 15):
        print(f"{name}: {i!s}")
        await asyncio.sleep(0.5)

async def main():
    tasks = []
    for n in range(0, 4):
        tasks.append(asyncio.create_task(counter(f"task{n}")))

    while True:
        tasks = [t for t in tasks if not t.done()]
        print('Main_loop')
        if len(tasks) == 0:
            return

        await tasks[0]




if __name__ == '__main__':

    asyncio.run(main())

    #from flowchem.client.client import get_all_flowchem_devices



    #flowchem_devices = get_all_flowchem_devices()

    #pump = flowchem_devices['my-plugin-device'].components['pump1']
    #valve = flowchem_devices['my-plugin-device'].components['valve']

    #pump.put("infuse", params={"rate": "3", "volume": "4"})


