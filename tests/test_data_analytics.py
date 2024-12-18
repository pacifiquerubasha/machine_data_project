import unittest
import os
import json
import logging
import tempfile
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Update the import to match the project structure
from analytics.data_analytics import calculate_average, detect_anomalies, analyze_data

class TestDataAnalytics(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test method."""
        # Create a temporary directory to simulate data folder
        self.test_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.test_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        logger.info(f"setUp: Created temporary test directory {self.test_dir}")

    def tearDown(self):
        """Clean up test environment after each test method."""
        # Remove temporary files and directories
        for file in os.listdir(self.data_dir):
            os.unlink(os.path.join(self.data_dir, file))
        os.rmdir(self.data_dir)
        os.rmdir(self.test_dir)
        logger.info(f"tearDown: Cleaned up temporary test directory {self.test_dir}")

    def test_calculate_average_normal(self):
        """Test calculate_average with a normal list of values."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        expected = 3.0
        result = calculate_average(values)
        self.assertEqual(result, expected)
        logger.info(f"test_calculate_average_normal: Success. Average of {values} is {result}")

    def test_calculate_average_empty_list(self):
        """Test calculate_average with an empty list."""
        values: List[float] = []
        expected = 0
        result = calculate_average(values)
        self.assertEqual(result, expected)
        logger.info("test_calculate_average_empty_list: Success. Empty list returns 0")

    def test_calculate_average_single_value(self):
        """Test calculate_average with a single value."""
        values = [42.5]
        expected = 42.5
        result = calculate_average(values)
        self.assertEqual(result, expected)
        logger.info(f"test_calculate_average_single_value: Success. Single value {values[0]} returned")

    def test_detect_anomalies_no_anomalies(self):
        """Test detect_anomalies with values close to the mean."""
        values = [10.0, 10.5, 9.8, 10.2, 9.9]
        anomalies = detect_anomalies(values)
        self.assertEqual(len(anomalies), 0)
        logger.info(f"test_detect_anomalies_no_anomalies: Success. No anomalies detected in {values}")

    def test_detect_anomalies_with_anomalies(self):
        """Test detect_anomalies with clear anomalies."""
        values = [10.0, 10.5, 50.0, 10.2, 9.9]
        anomalies = detect_anomalies(values)
        
        # Verify anomalies are detected
        self.assertTrue(len(anomalies) > 0, "Expected at least one anomaly")
        
        # Log detailed anomaly information
        logger.info(f"test_detect_anomalies_with_anomalies: Success.")
        logger.info(f"Anomalies detected: {anomalies}")

    def test_detect_anomalies_custom_threshold(self):
        """Test detect_anomalies with a custom threshold."""
        values = [10.0, 10.5, 11.5, 10.2, 9.9]
        anomalies = detect_anomalies(values, threshold=0.1)
        self.assertTrue(len(anomalies) > 0, "Expected at least one anomaly")
        
        # Log anomalies
        logger.info(f"test_detect_anomalies_custom_threshold: Success.")
        logger.info(f"Anomalies detected with custom threshold: {anomalies}")

    def test_detect_anomalies_insufficient_data(self):
        """Test detect_anomalies with insufficient data."""
        values = [10.0]
        anomalies = detect_anomalies(values)
        self.assertEqual(len(anomalies), 0)
        logger.info("test_detect_anomalies_insufficient_data: Success. No anomalies with insufficient data")

    def test_analyze_data_valid_data(self):
        """Test analyze_data with valid JSON input."""
        # Prepare test data with clear anomalies
        test_data = [
            {'temperature': 25.0, 'speed': 50.0, 'timestamp': '2023-01-01 00:00:00'},
            {'temperature': 26.0, 'speed': 55.0, 'timestamp': '2023-01-01 00:01:00'},
            {'temperature': 100.0, 'speed': 80.0, 'timestamp': '2023-01-01 00:02:00'}
        ]
        
        # Write test data to a temporary JSON file
        test_filename = 'test_machine_data.json'
        test_filepath = os.path.join(self.data_dir, test_filename)
        
        with open(test_filepath, 'w') as f:
            json.dump(test_data, f)

        # Temporarily patch the base directory for testing
        import analytics.data_analytics as data_analytics
        original_dirname = data_analytics.os.path.dirname
        data_analytics.os.path.dirname = lambda x: self.test_dir

        try:
            # Analyze the test data
            analysis = analyze_data(test_filename)

            # Verify analysis results
            self.assertIn('temperature', analysis)
            self.assertIn('speed', analysis)
            self.assertIn('period', analysis)

            # Check temperature analysis
            self.assertAlmostEqual(analysis['temperature']['average'], 50.33, places=2)
            self.assertEqual(analysis['temperature']['min'], 25.0)
            self.assertEqual(analysis['temperature']['max'], 100.0)
            self.assertEqual(analysis['temperature']['total_readings'], 3)
            
            # Verify there are anomalies
            temperature_anomalies = analysis['temperature']['anomalies']
            self.assertTrue(len(temperature_anomalies) > 0, "Expected temperature anomalies")
            
            # Log detailed analysis
            logger.info("test_analyze_data_valid_data: Success.")
            logger.info(f"Temperature analysis: {analysis['temperature']}")
            logger.info(f"Speed analysis: {analysis['speed']}")

        finally:
            # Restore the original dirname method
            data_analytics.os.path.dirname = original_dirname

    def test_analyze_data_file_not_found(self):
        """Test analyze_data with a non-existent file."""
        # Temporarily patch the base directory for testing
        import analytics.data_analytics as data_analytics
        original_dirname = data_analytics.os.path.dirname
        data_analytics.os.path.dirname = lambda x: self.test_dir

        try:
            # Attempt to analyze a non-existent file
            analysis = analyze_data('non_existent_file.json')
            self.assertEqual(analysis, {})
            logger.info("test_analyze_data_file_not_found: Success. Handled non-existent file")
        finally:
            # Restore the original dirname method
            data_analytics.os.path.dirname = original_dirname

    def test_analyze_data_empty_dataset(self):
        """Test analyze_data with an empty dataset."""
        # Prepare empty test data
        test_data = []
        
        # Write empty test data to a temporary JSON file
        test_filename = 'empty_machine_data.json'
        test_filepath = os.path.join(self.data_dir, test_filename)
        
        with open(test_filepath, 'w') as f:
            json.dump(test_data, f)

        # Temporarily patch the base directory for testing
        import analytics.data_analytics as data_analytics
        original_dirname = data_analytics.os.path.dirname
        data_analytics.os.path.dirname = lambda x: self.test_dir

        try:
            # Verify that an empty dataset raises a ValueError
            with self.assertRaises(ValueError):
                analyze_data(test_filename)
            logger.info("test_analyze_data_empty_dataset: Success. Raised ValueError for empty dataset")
        finally:
            # Restore the original dirname method
            data_analytics.os.path.dirname = original_dirname

if __name__ == '__main__':
    unittest.main()