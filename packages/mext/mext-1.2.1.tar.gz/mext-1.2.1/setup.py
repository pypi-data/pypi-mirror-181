import setuptools

README = open('README.md').read()

setuptools.setup(
    name='mext',
    version='1.2.1',
    url='https://github.com/modbender/manga-extractor',
    description='A simple manga extractor. Extracts any comic info, chapter list and chapter pages. In development.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Yashas H R',
    author_email='rameshmamathayashas@gmail.com',
    packages=setuptools.find_packages(),
    package_dir={'mext': 'mext'},
    package_data={
        'mext': ['data/*.json'],
    },
    install_requires=[
        'lxml>=4.6.0',
        'beautifulsoup4>=4.10.0',
        'undetected-chromedriver>=3.1.6',
        'pyvirtualdisplay>=2.2',
        'easyprocess>=1.0',
        'pillow>=9.1.0',
    ],
    python_requires='>=3.5',
    platforms=['any'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
