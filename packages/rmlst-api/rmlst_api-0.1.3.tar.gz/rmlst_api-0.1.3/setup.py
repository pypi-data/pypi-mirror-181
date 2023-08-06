from setuptools import setup

setup(
    name='rMLST-API',
    version='0.1.2',
    py_modules=['rmlst_api.*'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'rmlst_api = rmlst_api.cli:run_all',
        ],
    },
)