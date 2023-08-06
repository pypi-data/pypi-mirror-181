from os import path
from setuptools import setup


try:
    current_path = path.abspath(path.dirname(__file__))
except NameError:
    current_path = None


try:
    with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''


setup(
    name='op_package',
    version='1.0',
    license='MIT License',
    author='nazarbekov_1',
    author_email='nazarbekov04@inbox.ru',
    description='cocktail_sorting',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['tests'],
    python_requires='>=3.5',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'main=op_package:__main__',
            'cocktail_sort_increasing = '
            'op_package.sort_ascending:cocktail_sort_increasing',
            'cocktail_sort_decreasing = '
            'op_package.sort_descending:cocktail_sort_decreasing'
        ],
    },
)
