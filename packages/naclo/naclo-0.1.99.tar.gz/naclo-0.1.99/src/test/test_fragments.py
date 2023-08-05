import unittest
from naclo import fragments as frag
from naclo.mol_conversion import *


class TestFragments(unittest.TestCase):
    def test_frag_remover(self):
        # Test case
        test_smile = 'CCC.C.C'
        
        # Test all frag removing methods
        self.assertEqual(
            frag.mw(test_smile), 
            'CCC'
        )
        self.assertEqual(
            frag.atom_count(test_smile), 
            'CCC'
        )
        self.assertEqual(
            frag.carbon_count(test_smile),
            'CCC'
        )
        
    def test_remove_salts(self):
        # Test case
        test_mols = smiles_2_mols(['CN(C)C.Cl', 'CN(C)C.N'])
        
        # Test default salts [Cl,Br]
        self.assertEqual(
            mols_2_smiles(frag.remove_salts(test_mols)), 
            ['CN(C)C', 'CN(C)C.N']
        )
        
        # Test custom salts [N]
        self.assertEqual(
            mols_2_smiles(frag.remove_salts(test_mols, salts='[N]')), 
            ['CN(C)C.Cl', 'CN(C)C']
        )
        
        # Test no salts
        self.assertEqual(
            mols_2_smiles(frag.remove_salts(smiles_2_mols(['Cl', 'Br']))),
            ['', '']
        )
        
        # Doesn't remove when covalently bonded
        self.assertEqual(
            mols_2_smiles(frag.remove_salts(smiles_2_mols(['CCCCl']))),
            ['CCCCl']
        )
        
    def test_remove_recognized_salts(self):
        test_smiles = [
            'NC(CO)(CO)CO.CCC',
            'CCC',
            '[Ra].CCC'
        ]
        
        expected = 3*['CCC']
        out = [frag.remove_recognized_salts(s) for s in test_smiles]
        
        self.assertEqual(
            out,
            expected
        )

if __name__ == '__main__':
    unittest.main()
