from setuptools import setup

setup(
    name='neat-sciplots',
    version='0.1.0',
    packages=['src'],
    url='https://github.com/andreasfuhr/neat-sciplots',
    license='MIT',
    author='Andreas Führ',
    author_email='andreas.fuhr@outlook.com',
    description='Neatly format Matplotlib scientific plots',
    python_requires='>=3.4',
    install_requires=['matplotlib>=3.3.4', 'pyyaml', 'seaborn'],
)
