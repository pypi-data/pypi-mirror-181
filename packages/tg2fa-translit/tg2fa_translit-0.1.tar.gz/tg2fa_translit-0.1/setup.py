from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
            name='tg2fa_translit',
            version='0.1',
            author='stibiumghost',
            description='Translate Tajik texts to Persian with the help of a seq2seq model',
            long_description=long_description,
            long_description_content_type="text/markdown",
            packages=find_packages(),
            include_package_data=True
)