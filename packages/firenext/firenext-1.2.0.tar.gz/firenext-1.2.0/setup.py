from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12'

]

setup(
    name='firenext',
    version='1.2.0',
    description='This is an offline database library.',
    long_description=open("README.md").read() + "\n\n" +
                     open("CHANGELOG.txt").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/almoaz/PyFireNext',
    author='Mahfuz Salehin Moaz',
    author_email='almuaz1998@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='firenext',
    packages=find_packages()

)
