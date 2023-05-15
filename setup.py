from setuptools import setup

setup(
    name='desci-fetch',
    version='0.0.1',
    description='Import immutable code from DeSci Nodes code components',
    url='https://github.com/desci-labs/desci-fetch',
    author='DeSci Labs',
    author_email='sina@desci.com',
    license='MIT',
    packages=['desci'],
    install_requires=['pandas',
                      'requests',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
