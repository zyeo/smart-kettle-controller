import asyncio
import serial
import os
from dotenv import load_dotenv
from tapo import ApiClient

TARGET_TEMP = 55.0   # °C target to stop kettle
PORT = "/dev/cu.usbserial-14140" 
BAUD = 115200

async def main():
    load_dotenv()
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("IP_ADDRESS")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)

    ser = serial.Serial(PORT, BAUD, timeout=1)
    print("Connected to ESP32 and Tapo plug")

    device_on = False

    try:
        # --- turn on plug ---
        await device.on()
        device_on = True
        print("Kettle ON")

        while True:
            line = ser.readline().decode().strip()
            if not line:
                continue
            try:
                temp = float(line)
                print(f"Temp: {temp:.2f}°C")
            except ValueError:
                continue

            if temp >= TARGET_TEMP:
                print("Target temp reached — turning OFF")
                await device.off()
                device_on = False
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # safety cleanup
        if device_on:
            print("Safety shutdown — turning OFF plug.")
            try:
                await device.off()
            except Exception as e:
                print(f"Failed to turn off device safely: {e}")

        ser.close()
        print("Serial closed. Done.")


if __name__ == "__main__":
    asyncio.run(main())