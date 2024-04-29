import json
from datetime import datetime
from escpos.printer import Usb
import barcode
from barcode.writer import ImageWriter
import usb.util

def print_struk(barcode_data):
    # Load configuration from JSON file
    def load_config(file_path='config.json'):
        with open(file_path) as file:
            return json.load(file)

    config = load_config()

    # Initialize the USB printer
    # Replace 'idVendor' and 'idProduct' with the values from listdevs
    p = Usb(0x0fe6, 0x811e)

    # Print company header
    p.set(align='center', font='a', width=1, height=1)
    p.text(f"{config['nama_perusahaan']}\n{config['lokasi_parkir']}\n\n")

    # Print entrance ID and timestamp
    p.set(align='left', font='b', width=2, height=2)
    now = datetime.now()
    p.text(f"Entrance ID: {config['id_pintu_Masuk']}\n")
    p.text(now.strftime('%Y-%m-%d %H:%M:%S') + "\n\n")

    # Generate barcode
    code128 = barcode.Code128(barcode_data, writer=ImageWriter())
    barcode_buffer = code128.render()

    # Print barcode
    endpoint_address = 0x81
    endpoint_address_int = usb.util.endpoint_address(endpoint_address)
    p.image(barcode_buffer, impl='bitImageRaster', fragment_height=256, in_ep=endpoint_address_int)

    # Cut the paper
    p.cut()

# Example usage
# print_struk("1234567890128")
