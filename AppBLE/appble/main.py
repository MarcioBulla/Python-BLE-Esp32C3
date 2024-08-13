import asyncio
from bleak import BleakScanner, BleakClient

# UUID da característica que você deseja ler e escrever
UUID = "f5580f27-af8f-4796-b4ed-47600d173ce9"

async def send_command(client, command):
    await client.write_gatt_char(UUID, command.encode())
    print(f"Command '{command}' sent")

async def read_characteristic(client):
    value = await client.read_gatt_char(UUID)
    print(f"Characteristic value: {value.decode()}")

async def scan_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for i, device in enumerate(devices):
        print(f"{i + 1}: {device.name} ({device.address})")
    return devices

def print_menu():
    menu = """
    Options Menu:
C: Connect to a BLE device
O: Send 'ON' command
F: Send 'OFF' command
R: Read characteristic
P: Send a personalized message
D: Disconnect from the current BLE device
M: Print menu
Q: Quit
"""
    print(menu)

async def main():
    client = None
    ble_address = None
    print_menu()
    
    while True:
        choice = input("Select an option: ").strip().upper()

        if choice == 'C':
            devices = await scan_devices()
            if not devices:
                print("No BLE devices found.")
                continue
            
            try:
                device_index = int(input("Select the number of the device to connect: ")) - 1
                if device_index < 0 or device_index >= len(devices):
                    print("Invalid selection.")
                    continue
                
                ble_address = devices[device_index].address
            except ValueError:
                print("Invalid input.")
                continue

            print(f"Connecting to device {ble_address}.")
            
            try:
                async with BleakClient(ble_address) as client:
                    if client.is_connected:
                        print(f"Connected to device {ble_address}")
                        while True:
                            choice = input("Select an option: ").strip().upper()
                            
                            if choice == 'O':
                                await send_command(client, 'ON')

                            elif choice == 'F':
                                await send_command(client, 'OFF')

                            elif choice == 'R':
                                await read_characteristic(client)

                            elif choice == 'P':
                                personalized_message = input("Enter the personalized message to send: ")
                                await send_command(client, personalized_message)

                            elif choice == 'D':
                                await client.disconnect()
                                print("Disconnected from the BLE device.")
                                break  # Exit inner loop to allow reconnect or quit

                            elif choice == 'H':
                                print_menu()

                            elif choice == 'Q':
                                print("Quitting...")
                                return  # Exit outer loop to quit program
                            elif choice == 'C':
                                print("You are already connected to a device.")
                            else:
                                print("Invalid option. Please choose a valid letter option.")
            
            except Exception as e:
                print(f"Failed to connect or communicate with the BLE device: {e}")

        elif choice == 'Q':
            print("Quitting...")
            break

        else:
            print("Invalid option. Please choose a valid letter option.")


if __name__ == "__main__":
    asyncio.run(main())
