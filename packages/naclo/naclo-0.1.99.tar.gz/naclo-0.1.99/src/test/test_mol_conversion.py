import unittest
from naclo import mol_conversion
from rdkit.Chem import PandasTools
from rdkit import DataStructs
import pandas as pd
import numpy as np


class TestMolConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Load excel test data
        test_excel = pd.read_excel('test/assets/excel_test_case.xlsx')
        cls.excel_smiles = list(test_excel.Smiles)
        cls.excel_inchi_keys = list(test_excel.InChi)

        # Load SDF test data
        test_sdf = PandasTools.LoadSDF('test/assets/sdf_test_case.sdf', molColName='Molecule')
        cls.sdf_mols = list(test_sdf.Molecule)
        cls.sdf_smiles = list(test_sdf.Smiles)
        
        return super().setUpClass()
    
    def test_mols_2_smiles(self):
        self.assertEqual(
            self.sdf_smiles, 
            mol_conversion.mols_2_smiles(self.sdf_mols)
        )
        
    def test_smiles_2_mols(self):
        self.assertEqual(
            self.excel_smiles,
            mol_conversion.mols_2_smiles(mol_conversion.smiles_2_mols(self.excel_smiles))
        )
        
    def test_mols_2_inchi_keys(self):
        self.assertEqual(
            self.excel_inchi_keys,
            mol_conversion.mols_2_inchi_keys(mol_conversion.smiles_2_mols(self.excel_smiles))
        )
        
    def test_smiles_2_inchi_keys(self):
        self.assertEqual(
            self.excel_inchi_keys, 
            mol_conversion.smiles_2_inchi_keys(self.excel_smiles)
        )

    def test_mols_2_ecfp(self):
        ecfp = mol_conversion.mols_2_ecfp(self.sdf_mols, return_numpy=True)
        self.assertIsInstance(ecfp[0], np.ndarray)
        self.assertEqual(len(ecfp[0]), 1024)
        
        print_objs = mol_conversion.mols_2_ecfp(self.sdf_mols, return_numpy=False)
        self.assertIsInstance(print_objs[0], DataStructs.cDataStructs.ExplicitBitVect)
        
        print_objs = mol_conversion.mols_2_ecfp(self.sdf_mols, n_bits=None, return_numpy=False)
        self.assertIsInstance(print_objs[0], DataStructs.cDataStructs.UIntSparseIntVect)
        
        with self.assertWarns(UserWarning):
            print_objs = mol_conversion.mols_2_ecfp(self.sdf_mols, n_bits=None, return_numpy=True)
        
    def test_mols_2_maccs(self):
        maccss = mol_conversion.mols_2_maccs(self.sdf_mols)
        self.assertIsInstance(
            maccss[0],
            DataStructs.cDataStructs.ExplicitBitVect
        )
        
    def test_mols_2_ecfp_plus_descriptors(self):
        other_df = pd.DataFrame({
            'other1': [1, 3, 9, 22],
            'other2': [0.4, 0.77, 0.9, 0.01]
        })
        
        # Z norm
        out = mol_conversion.mols_2_ecfp_plus_descriptors(self.sdf_mols, other_df)


if __name__ == '__main__':
    unittest.main()
