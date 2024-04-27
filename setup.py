from setuptools import setup, find_packages

setup(
    name='ingate-python',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
       
    ],
    dependency_links=['file:///d:/lib/dependencies'],

    entry_points={
        'console_scripts': [
            'ingate-python = app:main',
        ],
    },
    author='niemubarok',
    author_email='niemubarok@email.com',
    description='ingate app',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/niemubarok/ingate-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
