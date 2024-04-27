from app import app


if __name__ == '__main__':
    # Start background thread to listen pin status
    pin_status_thread = threading.Thread(target=hardware_control.listen_input_pins, daemon=True)
    pin_status_thread.start()
    # database_operations.store_data_transaksi(1)
    
    # Start Flask server
    app.run(debug=True, port=5000)