import unittest
import numpy as np
import pandas as pd
from math import log10

import naclo
from naclo import UnitConverter


class TestUnitConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_values = [
            55,
            4,
            7,
            100,
            2000
        ]
        cls.test_units = [
            'ug•ml-1',
            'mg/l',
            'unrecognized',
            np.nan,
            'pm'
        ]
        cls.test_vivo_units = [
            'g/kg',
            'mg/kg',
            'mol/kg',
            'mmol/kg',
            'm'
        ]
        cls.test_mws = [
            220,
            400,
            300,
            110,
            150
        ]
        cls.test_smiles = 5*['CCC']
        cls.test_mols = naclo.smiles_2_mols(cls.test_smiles)
        
        cls.unit_converter = UnitConverter(cls.test_values, cls.test_units, cls.test_mws)
        cls.vivo_unit_converter = UnitConverter(cls.test_values, cls.test_vivo_units, cls.test_mws)
        return super().setUpClass()
    
    def test_to_molar_conversions(self):
        expected = np.array([
            250e-6,
            10e-6,
            np.nan,
            np.nan,
            2000e-12
        ])
        
        # Test all molar prefixes
        molars = self.unit_converter.to_molar()
        milli_molars = self.unit_converter.to_milli_molar()
        micro_molars = self.unit_converter.to_micro_molar()
        nano_molars = self.unit_converter.to_nano_molar()
        
        for vals, multi in zip([molars, milli_molars, micro_molars, nano_molars],
                               [1, 1e3, 1e6, 1e9]):
            self.assertIsInstance(
                vals,
                pd.Series
            )
            self.assertTrue(
                np.allclose(
                    vals.to_numpy(),
                    expected*multi,
                    equal_nan=True  # np.nan does not evaluate equal
                )
            )
            
    def test_to_mol_kg_conversions(self):
        expected = np.array([
            self.test_values[0]/self.test_mws[0],
            10e-6,
            7,  # mol/kg already
            100e-3,
            np.nan  # vitro unit not vivo (M)
        ])
        
        # Test all prefixes
        mol_kgs = self.vivo_unit_converter.to_mol_kg()
        mmol_kgs = self.vivo_unit_converter.to_milli_mol_kg()
        
        for vals, multi in zip([mol_kgs, mmol_kgs], [1, 1e3]):
            self.assertIsInstance(
                vals,
                pd.Series
            )
            self.assertTrue(
                np.allclose(
                    vals.to_numpy(),
                    expected*multi,
                    equal_nan=True  # np.nan does not evaluate equal
                )
            )
        
    def test_to_neg_log_molar(self):
        neg_log_molars = self.unit_converter.to_neg_log_molar()
        
        self.assertIsInstance(
            neg_log_molars,
            pd.Series
        )
        
        expected = np.array([
            3.60206,
            5,
            np.nan,
            np.nan,
            8.69897
        ])
        
        self.assertTrue(
            np.allclose(
                neg_log_molars.to_numpy(),
                expected,
                equal_nan=True
            )
        )
        
    def test_to_neg_log_mol_kg(self):
        neg_logs = self.vivo_unit_converter.to_neg_log_mol_kg()
        
        self.assertIsInstance(
            neg_logs,
            pd.Series
        )
        
        expected = np.array([
            -1*log10(self.test_values[0]/self.test_mws[0]),
            -1*log10(1e-3*self.test_values[1]/self.test_mws[1]),
            -1*log10(self.test_values[2]),
            -1*log10(1e-3*self.test_values[3]),
            np.nan
        ])
        
        self.assertTrue(
            np.allclose(
                neg_logs.to_numpy(),
                expected,
                equal_nan=True
            )
        )
        
    def test_df_converter(self):
        # Dont drop NA
        df = pd.DataFrame({'value': self.test_values, 'unit': self.test_units, 'mol': self.test_mols})
        out, col_name = UnitConverter.df_converter(df, 'mol', 'value', 'unit', 'm', drop_na_units=False)
        
        self.assertIn(
            'molar_value',
            out.columns
        )
        self.assertEqual(
            out['molar_value'].iloc[-1],
            df['value'].iloc[-1] * 1e-12  # pM
        )
        self.assertEqual(
            col_name,
            out.columns[-1],
            'molar_value'
        )
        
        # Drop NA indices
        out, col_name = UnitConverter.df_converter(df, 'mol', 'value', 'unit', 'm', drop_na_units=True)
        self.assertEqual(
            list(out.index),
            [0, 1, 4]
        )
        self.assertEqual(
            col_name,
            out.columns[-1],
            'molar_value'
        )
        
    def test_convert(self):
        # Test molar values --> -log(M) w/ case insensitivity
        units = ['M', 'mM', 'uM', 'nM', 'µM']
        for unit in units + [u.lower() for u in units] + [u.upper() for u in units[:-1]]:  # DONT CAP THE MU
            out = UnitConverter.convert(self.test_values, unit, '-log(m)')
            self.assertIsInstance(out, list)
            
        # Test g/L values
        g_ovr_l_units = ['g/l', 'mg/L', 'ug/L', 'ng/L']
        g_ovr_l_test_values = [5]
        test_mws = [100]
        molars = [5/100, 5e-3/100, 5e-6/100, 5e-9/100]
        
        for u, m in zip(g_ovr_l_units, molars):
            self.assertAlmostEqual(
                UnitConverter.convert(g_ovr_l_test_values, u, 'm', test_mws)[0],
                m
            )
        
        # No change
        self.assertEqual(
            UnitConverter.convert(g_ovr_l_test_values, 'g/l', 'g/l', test_mws),
            g_ovr_l_test_values
        )
        
        # print(self.test_values)
        # mws = []
        # for unit in units + [u.lower() for u in units] + [u.upper() for u in units[:-1]]:
        
        # ERROR: invalid input unit
        with self.assertRaises(ValueError):
            UnitConverter.convert(self.test_values, 'unrecognized', '-log(m)')
        
        # ERROR: invalid output unit
        with self.assertRaises(ValueError):
            UnitConverter.convert(self.test_values, 'm', 'unrecognized')

        
if __name__ == '__main__':
    unittest.main()
