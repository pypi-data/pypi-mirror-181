# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open


version = '0.3.1'
setup(

    name='divlibgithub3apps',

    version=version,
    packages=find_packages(),

    description='Access the Github API as an Application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.9',

    author='OneDiversified',
    author_email='support@onediversified.com',
    url='https://github.com/onediversified/div.lib.github3apps',
    download_url="https://github.com/onediversified/div.lib.github3apps/archive/v%s.tar.gz" % version,
    keywords='automation github apps git',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',

        'Programming Language :: Python :: 3',
    ],

    install_requires=[
        'cryptography>=3.4.8',
        'github3.py>=3.2.0',
        'pyjwt>=1.5.3',
        'requests>=2.18.0',
    ],

    extras_require={
        'dev': [
            'pypandoc',
            'twine',
            'wheel'
        ],
    }
)
