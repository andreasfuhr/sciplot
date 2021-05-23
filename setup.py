import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sciplot',
    version='0.8.1',
    author='Andreas Führ',
    author_email='andreas.fuhr@outlook.com',
    license='MIT',
    description='Format Matplotlib scientific plots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andreasfuhr/sciplot',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Framework :: Matplotlib',
        'Topic :: Scientific/Engineering'
    ],
    packages=['sciplot'],
    package_data={'sciplot': ['parameters/*.yml', '../README.md']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=['matplotlib>=3.3.4', 'pyyaml', 'seaborn'],
)
