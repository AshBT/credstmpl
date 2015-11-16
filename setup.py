from setuptools import setup

# cribbed from the lovely folks at https://github.com/LuminalOSS/credstash
setup(
    name='credstmpl',
    version='0.1.1'
    author = ['Eric Chu', 'Sang Han'],
    author_email = ['eric@qadium.com', 'sang@qadium.com'],
    description='A command-line tool to instantiate templates from credstash and lastpass',
    license='Apache v2',
    url='https://github.com/qadium/credstmpl',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python'
        ],
    install_requires=[
        'credstash>=1.5.2',
        'jinja2>=2.8',
        'jmespath==0.7.1',
    ],
    packages=['credstmpl'],
    entry_points={
        'console_scripts': [
            'credstmpl = credstmpl:main'
            ]
        }
    )
