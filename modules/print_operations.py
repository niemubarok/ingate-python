import json
from escpos.printer import Usb
from datetime import datetime
from PIL import Image


def print_struk(barcode_data):
    def load_config(file_path='config.json'):
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    config = load_config()

    settings = config['printer_settings']
    try:
        printer = Usb(settings['vendor_id'], settings['product_id'],
                      timeout=0, in_ep=settings['endpoint_in'],
                      out_ep=settings['endpoint_out'])

        printer.set(align='center')
        printer.text(f"{config['nama_perusahaan']}\n"
                     f"{config['lokasi_parkir']}\n\n")

        printer.set(align='left')
        text = f"Entrance ID: {config['id_pintu_Masuk']}\n"
        text += datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        printer.text(text)

        barcode_image = Image.open(barcode_data)
        printer.image(barcode_image)

        printer.cut()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'printer' in locals():
            printer.close()



