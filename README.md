# smart-kettle-controller

Simple IoT project that stops an electric kettle at a target temperature.

Tech:
- Python
- ESP32
- Smart plug (w/ Tapo API)
- ds18b20 temp sensor

How it works:
- Reads temperature from sensor
- When threshold reached → turns off plug
- Maintains target temperature by reactivating when temperature drops below threshold
