from setuptools import setup, find_packages


setup(
    name='naclo',
    version='0.1.99',
    license='MIT',
    author='Jacob Gerlach',
    author_email='jwgerlach00@gmail.com',
    url='https://github.com/jwgerlach00/naclo',
    description='Cleaning toolset for small molecule drug discovery datasets',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'naclo': [
        'assets/bleach_model.yml',
        'assets/bleach_warnings.yml',
        'assets/binarize_default_params.json',
        'assets/binarize_default_options.json',
        'assets/recognized_bleach_options.json',
        'assets/recognized_binarize_options.json',
        'assets/recognized_units.json',
        'assets/recognized_salts.json',
    ]},
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
        'PyYAML',
        'rdkit',
        'rdkit_pypi',
        'schema',
        'stse',
    ],
)
