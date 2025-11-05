import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from tapo import ApiClient
from tapo.requests import EnergyDataInterval, PowerDataInterval


async def main():
    load_dotenv()
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("IP_ADDRESS")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)

    print("Turning device on...")
    await device.on()

    print("Waiting 2 seconds...")
    await asyncio.sleep(2)

    print("Turning device off...")
    await device.off()

    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
