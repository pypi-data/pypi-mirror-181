from setuptools import setup


setup(
    name='exotic-ld',
    version='3.0.0',
    author='David Grant and Hannah R Wakeford',
    author_email='hannah.wakeford@bristol.ac.uk',
    url='https://github.com/Exo-TiC/ExoTiC-LD',
    license='MIT',
    packages=['exotic_ld'],
    description='ExoTiC limb-darkening calculator',
    long_description='Calculate limb-darkening coefficients for specific '
                     'instruments, stars, and wavelength ranges.',
    package_data={
        '': ['README.rst', 'LICENSE']
    },
    install_requires=['numpy', 'scipy'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=True,
)
