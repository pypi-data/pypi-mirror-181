from schema import Schema, Or


bleach_schema = Schema({
    # Structure data
    'structure_col': str,
    'structure_type': Or('smiles', 'mol'),

    # Target data
    'target_col': Or(str, None),
    'input_units': Or('mixed', '-log(M)', '-log(mol/kg)', 'M', 'mM', 'µM', 'uM', 'nM', 'g/L', 'mg/L', 'mol/kg', 'mmol/kg', 'g/kg', 'mg/kg', '%', ''),
    'output_units': Or('-log(M)', '-log(mol/kg)', 'M', 'mM', 'µM', 'uM', 'nM', 'g/L', 'mg/L', 'mol/kg', 'mmol/kg', 'g/kg', 'mg/kg', '%', ''),
    'units_col': str,
    'assay_type': Or('vitro', 'vivo', 'percent'),
    'drop_na_units': bool,

    # Formatting
    'format_settings': {
        'duplicate_compounds': Or('average', 'remove', 'keep'),
        'append_columns': [Or('smiles', 'mol', 'inchi_key', 'mw')],
        'remove_header_chars': str,
        'remove_na_targets': bool
    },

    # Chemistry
    'chem_settings': {
        'neutralize_charge': bool,
        'desalt': bool,
        'fragment_filter': Or('carbon_count', 'atom_count', 'mw', 'none', '')
    }
})
