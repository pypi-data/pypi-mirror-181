import setuptools

package_name = "stochpro"

# Requirements
requirements_file = open("requirements.txt", 'r')
requirements = [i.strip() for i in requirements_file.readlines()]
test_requirements_file = open("./tests/requirements.txt", 'r')
test_requirements = [i.strip() for i in requirements_file.readlines()]
docs_requirements_file = open("./docs/requirements.txt", 'r')
docs_requirements = [i.strip() for i in requirements_file.readlines()]

# ReadMe
long_description = open("README.rst", "r").read()

url = "https://github.com/dsagolla/stochpro"
download_url = url + "/archive/main.zip"
documentation_url = "https://stochpro.readthedocs.io/en/latest/"
tracker_url = url + "/issues"

# Setup
setuptools.setup(
    name="stochpro",
    version="0.0.1",
    author="Daniel Sagolla",
    author_email="dsagolla@mailbox.org",
    description=r"Sampling from stochastic processes.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords='probability stochastic random sampling sample simulate ' +
                'simulating stochastic-process process gaussian ' +
                'gaussian-process brownian-motion ito ito-process',
    url=url,
    download_url=download_url,
    project_urls={
        "Documentation": documentation_url,
        "Source": url,
        "Tracker": tracker_url,
    },
    platforms=['Linux', 'OSX', 'Windows'],
    packages=setuptools.find_packages(
        where='src',
        exclude=('tests', 'docs')
    ),
    package_dir={'': 'src'},
    install_requires=requirements,
    python_requires='>=3.7',
    setup_requires=[
        'setuptools',
        'pytest-runner'],
    tests_require=[
        'pytest',
    ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': test_requirements,
        'docs': docs_requirements,
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
1
