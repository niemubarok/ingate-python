import json
import os
import time
import winsound
from modules import port_operations, print_operations
import multiprocessing
import subprocess
import base64
from modules.barcode_generation import generate_barcode, random_number
from modules.database_operations import store_data_transaksi


# membuat variable global yang dapat diakses dari function

loop1_status = False
loop2_status = False
struk_status = False
is_able_to_print = False
is_loop2_on = False


def write_to_port(address, value):
    port_operations.write_to_port(address, value)


def read_from_port(address):
    return port_operations.read_from_port(address)


def update_control_signal(bit, state):
    value = read_from_port(port_operations.CONTROL_REGISTER)
    if state == 'off':
        value |= (1 << bit)
    else:
        value &= ~(1 << bit)
    write_to_port(port_operations.CONTROL_REGISTER, value)

def simulate_input_pins(pin, status):
    global loop1_status, loop2_status, struk_status, is_able_to_print, is_loop2_on

    print(pin, status)

    if pin == 'loop1':
        loop1_status = status == 'on'
    elif pin == 'loop2':
        loop2_status = status == 'on'
    elif pin == 'struk':
        struk_status = status == 'on'
    elif pin == 'is_able_to_print':
        is_able_to_print = status == 'on'
    elif pin == 'is_loop2_on':
        is_loop2_on = status == 'on'
        # pin_value = 1

def read_input_pins():
    status_value = read_from_port(port_operations.DATA_REGISTER)
    data_value = read_from_port(port_operations.DATA_REGISTER + 1)
    return {
        'pin12': data_value == 95,
        'pin13': data_value == 111,
        'pin10': data_value == 63,
        'pin11': data_value == 255,
        'data_register': data_value
    }




def check_conditions(data_value):


    if data_value == 31  or data_value == 15 or (loop1_status and struk_status):  # LOOP1 dan STRUK ON, LOOP2 OFF
        # is_able_to_print=True
        # print(data_value)
        print("BISA PRINT")
        handle_struk_button()
        is_able_to_print = False
    # elif :  # LOOP1, STRUK, dan LOOP2 ON
    #     return "Loop1, Struk, dan Loop2 ON = print struk"
    elif data_value == 111 or data_value == 79 or loop2_status or (loop1_status and  loop2_status):  # Motor lewat gate, LOOP2 ON, LOOP1 dan STRUK MATI
        # isPrinted=False
        is_able_to_print=True
        # is_loop2_on=True
        print("loop2 nyala")
    # else:
    #     return "Tidak ada kondisi yang sesuai"

def listen_input_pins():
    while True:
        # pin_status = read_input_pins()
        # print_pin_status(pin_status)
        # app.config['pin_status'] = pin_status
        # data_value = read_from_port(port_operations.DATA_REGISTER + 1)  # Baca nilai data register
        # check_conditions(data_value)
        # handle_struk_button()
        if is_able_to_print:
            print("bisa print")
        else:
            # print("idle")
            pass

        time.sleep(1)  # Ganti dengan waktu polling yang sesuai

        # print_pin_status(pin_status)
        # if(pin_status) 
        # 1. jika loop1 dan struk on dan loop2 off (79)= bisa print
        # 2. loop1, struk dan loop 2 on (15) = bisa print
        # 3. ketika motor lewat gate, loop2 on, loop1 dan struk mati.

        # kondisi tidak bisa print
        # 1. 

def handle_struk_button():
    global is_able_to_print
    if is_able_to_print:
        print("Struk button pressed")
        barcode_data = random_number()
        if barcode_data is None:
            raise ValueError("barcode_data is None")

        barcode_image = generate_barcode(barcode_data)  
        if barcode_image is None:
            raise ValueError("barcode_image is None")

        store_data_transaksi(barcode_data)
        if barcode_data is None:
            raise ValueError("Failed to store barcode_data")

        print_operations.print_struk(barcode_image)
        if barcode_image is None:
            raise ValueError("Failed to print barcode_image")
        
        store_data_transaksi(barcode_data)

        
        print_operations.print_struk(barcode_image)


def run_audio(filename):

    folder_path = './static/sounds'
    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(file_path):
        print(f'Audio file {file_path} not found')
        return

    p = multiprocessing.Process(target=winsound.PlaySound, args=(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC))
    p.start()
    p.join()




def pic_body_masuk():
    snapshot_filename = 'snapshot.jpeg'
    with open('config.json', 'r') as f:
        config = json.load(f)
    snapshot_url = config['url_ctv']

    # Ambil snapshot dari CCTV
    if snapshot_url is not None:
        subprocess.run(['curl', snapshot_url, '-o', snapshot_filename])

    # Simpan gambar ke database
    with open(snapshot_filename, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

    # Hapus file snapshot
    os.remove(snapshot_filename)

    return img_base64


