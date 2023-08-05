import setuptools

setuptools.setup(
    name='archimedean',
    version='4.9',
    author='Daniel Li',
    author_email='daniel.miami2005@gmail.com',
    description='The Ultimate Archimedean CLI',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BananaApache/archimedean',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'click',
        'requests',
        'bs4',
        'PyPDF2',
        'pillow',
    ],
    scripts=['./bin/archimedean'],
    python_requires='>=3.6'
)