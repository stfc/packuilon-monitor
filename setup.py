from setuptools import setup, find_packages


setup(
    name='packuilon-monitor',
    version='0.1.0',
    description='A simple web monitor for Packuilon builds.',
    url='https://github.com/daantjie/packuilon-monitor',
    author='Daniel Oosthuizen',
    author_email='danieltheexperimenter@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License 3.0',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(exclude=['doc', 'test']),
    install_requires=[
        'humanize',
        'ansi2html',
        'flask'
    ],
    python_requires='>=2.7, <3',
    ## package_data=XXX
    entry_points={
        'console_scripts': [
            'packuilon-monitor=packuilon_monitor:main'
        ]
    }
    )
