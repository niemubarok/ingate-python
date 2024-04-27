import ctypes
import os

dll_path = os.path.join(os.getcwd(), 'lib', 'inpoutx64.dll')
if not os.path.exists(dll_path):
    raise FileNotFoundError("inpoutx64.dll not found in the 'lib' directory.")
inpout = ctypes.WinDLL(dll_path)

BASE_PORT = 0x378
CONTROL_REGISTER = BASE_PORT + 2
DATA_REGISTER = BASE_PORT

def write_to_port(address, value):
    inpout.Out32(address, value)

def read_from_port(address):
    return inpout.Inp32(address)
