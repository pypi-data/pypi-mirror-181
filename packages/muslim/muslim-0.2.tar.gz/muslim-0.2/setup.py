from setuptools import setup, find_packages

setup(
    name='muslim',
    version='0.2',
    license='CC0 1.0 Universal',
    author="Harsh Avinash",
    author_email='harsh.avinash.official@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Harsh-Avinash/pip-install-muslim',
    keywords='Muslims in python',
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy'
    ],

)
