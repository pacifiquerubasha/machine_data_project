import threading
from data_generator import continuous_data_generation
from data_processor import continuous_data_processing

def main():
    """
    Main application to run data generation and processing concurrently.
    """
    print("Starting Machine Data Monitoring System...")
    
    # Start data generation in a separate thread
    data_gen_thread = threading.Thread(
        target=continuous_data_generation, 
        kwargs={'interval': 10, 'filename': 'machine_data.json'}
    )
    data_gen_thread.daemon = True
    
    # Start data processing in a separate thread
    data_proc_thread = threading.Thread(
        target=continuous_data_processing, 
        kwargs={'interval': 10, 'filename': 'machine_data.json'}
    )
    data_proc_thread.daemon = True
    
    # Start both threads
    data_gen_thread.start()
    data_proc_thread.start()
    
    # Keep main thread running
    try:
        while True:
            threading.Event().wait()
    except KeyboardInterrupt:
        print("\nStopping Machine Data Monitoring System...")

if __name__ == "__main__":
    main()