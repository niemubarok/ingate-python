import datetime
import barcode 

# def generate_barcode():
#     random_number = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
#     barcode = get_barcode_class('ean13')
#     ean = barcode(random_number)
#     svg_text = ean.save('barcode.svg', scale=2, human_readable=True)
#     svg_text = ean.renderBase64()
#     return svg_text

def random_number():
    current_date = datetime.datetime.now()
    random_number = f"{current_date.year}{str(current_date.month).zfill(2)}{str(current_date.day).zfill(2)}{str(current_date.hour).zfill(2)}{str(current_date.minute).zfill(2)}{str(current_date.second).zfill(2)}"
    return random_number

def generate_barcode(data):
    # Implement your barcode generation logic using python-barcode library
    # For example, generate a Code 128 barcode with a random data
    code128 = barcode.get('code128', data)
    barcode_path = f'barcode_{data}'  # Save the barcode in PNG format
    code128.save(barcode_path) # save as png
    return barcode_path

