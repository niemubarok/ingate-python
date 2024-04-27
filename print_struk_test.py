import unittest
from unittest.mock import patch
from io import StringIO
from datetime import datetime
from PIL import Image
import json
from modules.print_operations import print_struk

class TestPrintStruk(unittest.TestCase):
    def setUp(self):
        self.mock_config = {
            "printer_settings": {
                "vendor_id": "your_vendor_id",
                "product_id": "your_product_id",
                "endpoint_in": "your_endpoint_in",
                "endpoint_out": "your_endpoint_out"
            },
            "nama_perusahaan": "Your Company",
            "lokasi_parkir": "Parking Location",
            "id_pintu_Masuk": "Entrance ID"
        }

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("usb.Usb")
    @patch("builtins.print")
    def test_print_struk(self, mock_print, mock_usb, mock_open):
        mock_open.return_value.read.return_value = json.dumps(self.mock_config)
        barcode_data = "barcode_image.jpg"
        expected_output = [
            f"{self.mock_config['nama_perusahaan']}\n{self.mock_config['lokasi_parkir']}\n\n",
            f"Entrance ID: {self.mock_config['id_pintu_Masuk']}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        ]
        print_struk(barcode_data)
        calls = [unittest.mock.call(text) for text in expected_output]
        mock_print.assert_has_calls(calls)
        mock_usb.assert_called_once()

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("usb.Usb", side_effect=Exception("USB Error"))
    @patch("builtins.print")
    def test_print_struk_exception(self, mock_print, mock_usb, mock_open):
        mock_open.return_value.read.return_value = json.dumps(self.mock_config)
        barcode_data = "barcode_image.jpg"
        print_struk(barcode_data)
        mock_print.assert_called_once_with("Error: USB Error")

if __name__ == "__main__":
    unittest.main()
