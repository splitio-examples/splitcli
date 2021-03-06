from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='splitcli',
    version='0.0.1',
    description='Use Split.io from the command line',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/splitio-examples/splitcli',
    author='Henry Jewkes &  Talia Nassi & Micah Silverman',
    author_email='info@split.io',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Feature Flags',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='development, split, feature flags',
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['requests', 'python-inquirer', 'art'],
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={  # Optional
        'console_scripts': [
            'splitcli=splitcli:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/splitio-examples/splitcli/issues',
        'Source': 'https://github.com/splitio-examples/splitcli',
    },
)