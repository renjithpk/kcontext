from setuptools import setup, find_packages

setup(
    name='kcontext',
    version='0.1.0',
    py_modules=['kcontext'],
    entry_points={
        'console_scripts': [
            'kcontext=kcontext:main',
        ],
    },
    author='renjith.pk',
    description='A Kubernetes context manager tool',
    url='https://github.com/renjithpk/kcontext',
    license='MIT',
)
