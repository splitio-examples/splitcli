from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='splitcli',
    version='0.0.9',
    description='Use Split.io from the command line',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/splitio-examples/splitcli',
    author='Henry Jewkes &  Talia Nassi & Micah Silverman',
    author_email='info@split.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='development, split, feature flags',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['requests', 'python-inquirer', 'art', 'inquirer'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'splitcli=splitcli.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/splitio-examples/splitcli/issues',
        'Source': 'https://github.com/splitio-examples/splitcli',
    },
)
