from setuptools import setup

setup(
    name='hashwd',
    version='0.11',
    py_modules=['hashwd'],
    include_package_data=True,
    install_requires=[
        'pyperclip',
        'argparse',
        'random'
    ],
    entry_points={
        'console_scripts': [
            'hashwd=hashwd:main'
        ]
    }
)