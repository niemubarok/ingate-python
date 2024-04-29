import json
import os
import threading
import time
import winsound
from modules import port_operations, print_operations
import multiprocessing
import subprocess
import base64
from modules.barcode_generation import generate_barcode, random_number
from modules.database_operations import store_data_transaksi


# membuat variable global yang dapat diakses dari function

loop1_status = True
loop2_status = True
struk_status = True
is_able_to_print = True
is_loop2_on = True


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

def open_gate():
    update_control_signal(0, 'on')
    time.sleep(0.5)
    update_control_signal(0, 'off')

def check_conditions(data_value):
    global loop1_status, loop2_status, struk_status, is_able_to_print
    if data_value == 95 and loop1_status:  # LOOP1 dan LOOP2 ON
        thread = threading.Thread(target=run_audio, args=('ticket_button.wav',))
        thread.start()
        thread.join()  # wait for the audio to finish playing
        loop1_status = False
        
        # run_audio('welcome.wav')

    elif (data_value == 31 and struk_status) or (data_value == 15 and struk_status) :  # LOOP1 dan STRUK ON, LOOP2 OFF
        # is_able_to_print=True
        # print(data_value)
        print("BISA PRINT")
        threading.Thread(target=run_audio, args=('welcome.wav',)).start()
        handle_struk_button()
        is_able_to_print = False
        struk_status = False
    # elif :  # LOOP1, STRUK, dan LOOP2 ON
    #     return "Loop1, Struk, dan Loop2 ON = print struk"
    elif data_value == 111 or data_value == 79: 
    # or loop2_status or (loop1_status and  loop2_status):  # Motor lewat gate, LOOP2 ON, LOOP1 dan STRUK MATI
        # isPrinted=False
        loop1_status = True
        is_able_to_print=True
        struk_status = True
        # is_loop2_on=True
        print("loop2 nyala")
    # else:
    #     return "Tidak ada kondisi yang sesuai"


def send_off_to_bits_0_and_3():
    update_control_signal(0, 'off')
    update_control_signal(3, 'off')

def listen_input_pins():
    while True:
        # pin_status = read_input_pins()
        # print_pin_status(pin_status)
        # app.config['pin_status'] = pin_status
        data_value = read_from_port(port_operations.DATA_REGISTER + 1)  # Baca nilai data register
        check_conditions(31)
        # handle_struk_button()
        # if is_able_to_print:
        #     print("iddle")
        # else:
        #     # print("idle")
        #     pass

        # Menggunakan selalu blok sleep(0) untuk tidak menggunakan polling
        # Dengan cara ini, kode akan terus berjalan tanpa menggunakan polling
        # Tapi pastikan tidak ada jaringan yang tidak berfungsi karena terlalu banyak thread yang terbuka
        # Jika ada jaringan yang tidak berfungsi, gunakan polling atau gunakan threading.Event untuk waktu polling
        # https://docs.python.org/3/library/time.html#time.sleep
        # https://docs.python.org/3/library/threading.html#threading.Event
        time.sleep(3)
        # time.sleep(4)  # Ganti dengan waktu polling yang sesuai

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

        
        store_data_transaksi(barcode_data)
        print_operations.print_struk(barcode_data)
        open_gate()

def run_audio(filename):
    folder_path = './static/sounds/'
    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(file_path):
        print(f'Audio file {file_path} not found')
        return

    try:
       winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except FileNotFoundError as e:
        print('Error running audio file:', str(e))
    except subprocess.CalledProcessError as e:
        print(f'Error running audio file: {e}')




def pic_body_masuk():
    snapshot_filenames = ['snapshot.jpg', 'snapshot.png', 'snapshot.jpeg']
    snapshot_file = next((filename for filename in snapshot_filenames if os.path.exists(filename)), None)
    if snapshot_file is None:
        print('Snapshot file not found')
        return
    snapshot_filename = snapshot_file
    with open('config.json', 'r') as f:
        config = json.load(f)
    snapshot_url = config['url_ctv'] if config.get('url_ctv') else None

    # Ambil snapshot dari CCTV
    if snapshot_url is not None:
        subprocess.run(['curl', snapshot_url, '-o', snapshot_filename])

    # Simpan gambar ke database
    with open(snapshot_filename, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

    # Hapus file snapshot
    # os.remove(snapshot_filename)
    # print(img_base64)
    return img_base64


