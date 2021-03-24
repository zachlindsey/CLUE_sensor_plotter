import asyncio
import time
from bleak import BleakScanner, BleakClient
from bleak.backends._manufacturers import MANUFACTURERS


async def scan_for_devices():
    devices = await BleakScanner.discover()
    for d in devices:
        print('---')
        print('Name:\t', d.name)
        print('Address:\t',d.address)
        print('RSSI:\t', d.rssi)
        print('UUIDS:')
        for uuid in d.metadata['uuids']:
            print('\t'+str(uuid))
        if "manufacturer_data" in d.metadata:
            ks = list(d.metadata["manufacturer_data"].keys())
            if len(ks):
                mf = MANUFACTURERS.get(ks[0], MANUFACTURERS.get(0xFFFF))
                value = d.metadata["manufacturer_data"].get(
                    ks[0], MANUFACTURERS.get(0xFFFF)
                )
                # TODO: Evaluate how to interpret the value of the company identifier...
                print("{0} ({1})".format(mf, value))

ADDRESS = "C5:DF:52:61:6F:19"
# 
async def run(address):
    client = BleakClient(address)
    try:
        await client.connect()
        print("Connceted!")
        rx_char = client.services.get_characteristic("8ba86974-935c-447c-91ad-bdcbad575f31")

        while True:
            color = input("input color hex:")
            if len(color) != 6:
                print('invalid hex length')
                continue
            try:
                hexcode = int(color, 16)
                await client.write_gatt_char(rx_char, color.encode('utf-8'))

            except ValueError:
                print("invalid hex string")
            time.sleep(1)

    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run(ADDRESS))


