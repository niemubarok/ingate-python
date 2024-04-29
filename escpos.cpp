#include <iostream>
#include <windows.h>
#include <SetupAPI.h>
#include <Usbiodef.h>

int main(int argc, char *argv[])
{
    // Pastikan argumen yang diberikan sesuai
    if (argc < 5)
    {
        std::cerr << "Usage: " << argv[0] << " VID PID TEXT" << std::endl;
        return 1;
    }

    // Ambil Vendor ID dan Product ID dari argumen
    DWORD vid = std::stoi(argv[1], nullptr, 16);
    DWORD pid = std::stoi(argv[2], nullptr, 16);

    // Initialize WinUSB
    HDEVINFO deviceInfo;
    SP_DEVICE_INTERFACE_DATA deviceInterfaceData;
    deviceInterfaceData.cbSize = sizeof(SP_DEVICE_INTERFACE_DATA);

    GUID interfaceClassGuid;
    InterfaceClassGuidFromName(L"USB", &interfaceClassGuid);

    deviceInfo = SetupDiGetClassDevs(&interfaceClassGuid, NULL, NULL, DIGCF_PRESENT | DIGCF_DEVICEINTERFACE);

    // Cari device printer berdasarkan VID dan PID
    DWORD index = 0;
    BOOL success = TRUE;
    SP_DEVINFO_DATA devInfoData;
    while (success)
    {
        success = SetupDiEnumDeviceInfo(deviceInfo, index, &devInfoData);
        if (success)
        {
            DWORD dataType;
            TCHAR dataBuffer[4096];
            success = SetupDiGetDeviceRegistryProperty(deviceInfo, &devInfoData, SPDRP_HARDWAREID, &dataType, reinterpret_cast<PBYTE>(dataBuffer), sizeof(dataBuffer), NULL);
            if (success && dataType == REG_SZ)
            {
                if (wcsstr(dataBuffer, L"VID_") != NULL && wcsstr(dataBuffer, L"PID_") != NULL)
                {
                    if (wcsstr(dataBuffer, std::to_wstring(vid).c_str()) != NULL && wcsstr(dataBuffer, std::to_wstring(pid).c_str()) != NULL)
                    {
                        break;
                    }
                }
            }
        }
        index++;
    }

    if (!success)
    {
        std::cerr << "Printer tidak ditemukan." << std::endl;
        SetupDiDestroyDeviceInfoList(deviceInfo);
        return 1;
    }

    // Buka koneksi ke printer
    HANDLE hDevice = CreateFile(L"\\\\.\\USB#VID_" + std::to_wstring(vid) + L"&PID_" + std::to_wstring(pid) + L"#{a5dcbf10-6530-11d2-901f-00c04fb951ed}", GENERIC_WRITE, FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hDevice == INVALID_HANDLE_VALUE)
    {
        std::cerr << "Gagal membuka koneksi ke printer." << std::endl;
        SetupDiDestroyDeviceInfoList(deviceInfo);
        return 1;
    }

    // Data teks yang akan dicetak
    const char *text = argv[3];

    // Kirim perintah ESC/POS untuk mencetak teks
    DWORD bytesWritten;
    BOOL result = WriteFile(hDevice, text, strlen(text), &bytesWritten, NULL);
    if (!result)
    {
        std::cerr << "Gagal mengirim data ke printer." << std::endl;
        CloseHandle(hDevice);
        SetupDiDestroyDeviceInfoList(deviceInfo);
        return 1;
    }

    // Tutup koneksi ke printer
    CloseHandle(hDevice);
    SetupDiDestroyDeviceInfoList(deviceInfo);

    std::cout << "Teks berhasil dicetak ke printer." << std::endl;
    return 0;
}
