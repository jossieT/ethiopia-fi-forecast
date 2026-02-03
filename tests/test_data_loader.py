import sys
import os
import unittest
import pandas as pd

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_loader import load_data

class TestDataLoader(unittest.TestCase):
    def test_load_data_structure(self):
        """Test that data_loader returns two dataframes with expected columns."""
        # Using a relative path that should work from project root (where pytest/unittest usually runs)
        # or relative to the test file if we handle it correctly.
        # The data_loader already handles some relative path logic.
        try:
            df, df_impact = load_data(data_path="data/raw/ethiopia_fi_unified_data.xlsx")
            
            # Check types
            self.assertIsInstance(df, pd.DataFrame)
            self.assertIsInstance(df_impact, pd.DataFrame)
            
            # Check essential columns
            self.assertIn('record_id', df.columns)
            self.assertIn('record_type', df.columns)
            self.assertIn('indicator_code', df.columns)
            
            self.assertIn('parent_id', df_impact.columns)
            self.assertIn('impact_direction', df_impact.columns)
            
        except FileNotFoundError:
            self.skipTest("Data file not found for testing - check paths.")

    def test_enrichment_logic(self):
        """Test that enrichment data is actually added."""
        try:
            df, _ = load_data()
            # We know EVT_NEW_01 is one of our enrichments
            self.assertTrue(any(df['record_id'] == 'EVT_NEW_01'))
        except FileNotFoundError:
            self.skipTest("Data file not found.")

if __name__ == '__main__':
    unittest.main()
