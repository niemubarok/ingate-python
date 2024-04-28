import datetime
import logging
from modules import db, hardware_control


def store_data_transaksi(random_number):

    lastIdQuery = "SELECT MAX(id) FROM transaksi_parkir"
    lastIdResult =  db.execute_query(lastIdQuery)
    lastId = lastIdResult[0][0] if lastIdResult[0][0] is not None else lastIdResult[0]
    newId = int(lastId) + 1
    # print(newId)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # random_number = barcode_generation.random_number()
    print(random_number)
    data_to_store = {
        "id": newId,
        "no_pol": random_number,
        "id_kendaraan": "A",
        "status": 1,
        "id_pintu_masuk": None,
        "id_pintu_keluar": None,
        "waktu_masuk": current_date,
        "waktu_keluar": None,
        "id_op_masuk": None,
        "id_op_keluar": None,
        "id_shift_masuk": None,
        "id_shift_keluar": None,
        "kategori": None,
        "status_transaksi": 0,
        "bayar_masuk": 0,
        "bayar_keluar": 0,
        "jenis_system": None,
        "tanggal": current_date,
        "pic_body_masuk": hardware_control.pic_body_masuk(),
        "pic_body_keluar": None,
        "pic_driver_masuk":None ,
        "pic_driver_keluar": None,
        "pic_no_pol_masuk": None,
        "pic_no_pol_keluar": None,
        "sinkron": None,
        "adm": None,
        "alasan": None,
        "pmlogin": None,
        "pklogin": None,
        "upload": None,
        "manual": None,
        "veri_kode": None,
        "veri_check": None,
        "veri_adm": None,
        "veri_date": None,
        "denda": None,
        "extra_bayar": None,
        "no_barcode": None,
        "jenis_langganan": None,
        "post_pay": None,
        "reff_kode": None,
        "valet_adm": None,
        "waktu_valet": None,
        "valet_charge": None,
        "valet_ops": None,
        "valet_nopol": None,
        "login_waktu_valet": None,
        "cara_bayar": None,
        "unit_member": None,
        "reserved": None,
        "no_voucher": None,
        "seri_voucher": None,
        "no_access_in": None,
        "no_access_out": None,
        "inap": None,
        # "casual_denda": None,
    }
    try:
        db.create('transaksi_parkir', data_to_store)
        logging.info(f'Data berhasil dimasukkan dengan ID: {newId}')
    except Exception as e:
        logging.error(f'Gagal memasukkan data. Error: {e}')
    return

def get_settings():
    query = "SELECT * FROM config_pos_hardware"
    result = db.execute_query(query)
    return result