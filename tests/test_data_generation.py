import unittest
import os
import json
import time
from datetime import datetime
import threading

# Import the functions to test
from data_process.data_generator import generate_machine_data, save_data_to_json, continuous_data_generation
import data_process.data_generator as data_generation

class TestMachineDataGeneration(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test method."""
        # Create a temporary directory to simulate data folder
        self.base_test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_folder = os.path.join(self.base_test_dir, 'data')
        os.makedirs(self.data_folder, exist_ok=True)
        
    def test_generate_machine_data(self):
        """Test generate_machine_data function."""
        # Generate data
        data = generate_machine_data()
        
        # Verify data structure and types
        self.assertIn('timestamp', data)
        self.assertIn('temperature', data)
        self.assertIn('speed', data)
        self.assertIn('status', data)
        
        # Check timestamp is valid ISO format
        try:
            datetime.fromisoformat(data['timestamp'])
        except ValueError:
            self.fail("Invalid timestamp format")
        
        # Check temperature range
        self.assertGreaterEqual(data['temperature'], 20.0)
        self.assertLessEqual(data['temperature'], 30.0)
        
        # Check speed range
        self.assertGreaterEqual(data['speed'], 40.0)
        self.assertLessEqual(data['speed'], 60.0)
        
        # Check status is one of the expected values
        self.assertIn(data['status'], ['IDLE', 'RUNNING', 'PAUSED'])
    
    def test_save_data_to_json(self):
        """Test save_data_to_json function."""
        # Filename for this test
        test_filename = 'test_machine_data.json'
        test_filepath = os.path.join(self.data_folder, test_filename)
        
        # Ensure clean test environment
        if os.path.exists(test_filepath):
            os.remove(test_filepath)
        
        # Save initial data
        first_data = save_data_to_json(test_filename, max_entries=3)
        
        # Verify file was created
        self.assertTrue(os.path.exists(test_filepath))
        
        # Read and verify contents
        with open(test_filepath, 'r') as f:
            saved_data = json.load(f)
        
        # Check data was saved correctly
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0], first_data)
        
        # Save more data to test max_entries
        for _ in range(5):
            save_data_to_json(test_filename, max_entries=3)
        
        # Reread file
        with open(test_filepath, 'r') as f:
            saved_data = json.load(f)
        
        # Verify max_entries works
        self.assertLessEqual(len(saved_data), 3)
    
    def test_continuous_data_generation(self):
        """Test continuous_data_generation function."""
        # Filename for this test
        test_filename = 'continuous_machine_data.json'
        test_filepath = os.path.join(self.data_folder, test_filename)
        
        # Ensure clean test environment
        if os.path.exists(test_filepath):
            os.remove(test_filepath)
        
        # Track generated threads
        generated_threads = []
        
        def mock_save_data_to_json(_filename):
            """Mock function to track thread creation."""
            generated_threads.append(threading.current_thread())
            save_data_to_json(_filename)
        
        # Monkey patch save_data_to_json temporarily
        # import data_generation
        original_save_func = data_generation.save_data_to_json
        data_generation.save_data_to_json = mock_save_data_to_json
        
        try:
            # Start continuous generation
            continuous_data_generation(interval=0.1, filename=test_filename)
            
            # Wait a bit to allow some threads to generate
            time.sleep(0.5)
            
            # Verify threads were created
            self.assertGreater(len(generated_threads), 1)
            
            # Verify file was created
            self.assertTrue(os.path.exists(test_filepath))
            
            # Verify file contains data
            with open(test_filepath, 'r') as f:
                saved_data = json.load(f)
            
            self.assertGreater(len(saved_data), 0)
        
        finally:
            # Restore original function
            data_generation.save_data_to_json = original_save_func
    
    def test_json_file_handling(self):
        """Test handling of existing and non-existing JSON files."""
        # Filename for this test
        test_filename = 'json_handling_test.json'
        test_filepath = os.path.join(self.data_folder, test_filename)
        
        # Ensure clean test environment
        if os.path.exists(test_filepath):
            os.remove(test_filepath)
        
        # Test saving to a non-existing file
        first_data = save_data_to_json(test_filename, max_entries=3)
        
        # Verify file was created
        self.assertTrue(os.path.exists(test_filepath))
        
        # Read and verify contents
        with open(test_filepath, 'r') as f:
            saved_data = json.load(f)
        
        # Check data was saved correctly
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0], first_data)
        
        # Simulate corrupted JSON file
        with open(test_filepath, 'w') as f:
            f.write('invalid json')
        
        # Try saving to a file with invalid JSON
        second_data = save_data_to_json(test_filename, max_entries=3)
        
        # Verify file was overwritten with valid data
        with open(test_filepath, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0], second_data)

if __name__ == '__main__':
    unittest.main()