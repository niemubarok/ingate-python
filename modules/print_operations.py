import json
import io
from datetime import datetime
from PIL import ImageFont, Image
import win32print
import win32ui
import barcode
from barcode.writer import ImageWriter

def print_struk(barcode_data):
    def load_config(file_path='config.json'):
        with open(file_path) as file:
            return json.load(file)

    config = load_config()

    font_size = 15
    font_path = 'C:/Windows/Fonts/arial.ttf'
    font = ImageFont.truetype(font_path, font_size)

    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        hprinterdc = win32ui.CreateDC()
        hprinterdc.CreatePrinterDC(printer_name)
        
        header = f"{config['nama_perusahaan']}\n{config['lokasi_parkir']}\n\n"
        hprinterdc.StartDoc("Receipt")
        hprinterdc.StartPage()
        
        # Draw company header
        hprinterdc.SelectObject(font)  # Set font
        hprinterdc.TextOut(100, 100, header)
        
        # Draw entrance ID and timestamp
        now = datetime.now()
        text = (
            f"Entrance ID: {config['id_pintu_Masuk']}\n"
            f"{now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        hprinterdc.TextOut(100, 200, text)
        
        # Generate and print barcode
        code128 = barcode.Code128(barcode_data, writer=ImageWriter())
        barcode_buffer = io.BytesIO()
        code128.write(barcode_buffer)
        barcode_image = Image.open(barcode_buffer)
        
        # Convert barcode image to monochrome (1-bit) for printing
        barcode_image = barcode_image.convert("1")
        
        # Get the dimensions of the barcode image
        width, height = barcode_image.size
        
        # Print the barcode image
        hprinterdc.StretchBlt((100, 300, 100 + width, 300 + height), barcode_image, (0, 0, width, height), win32con.SRCCOPY)
        
        hprinterdc.EndPage()
        hprinterdc.EndDoc()
    except Exception as e:
        print(f"Error with the printer: {str(e)}")
    finally:
        win32print.ClosePrinter(hprinter)

# Contoh pemanggilan fungsi
print_struk("1234567890")
