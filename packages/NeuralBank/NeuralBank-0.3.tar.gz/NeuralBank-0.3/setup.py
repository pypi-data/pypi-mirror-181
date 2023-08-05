from setuptools import setup, find_packages


setup(
    name='NeuralBank',
    version='0.3',
    license='MIT',
    author="NeuralBank",
    author_email='ziyad@neuralbank.ai',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='neuralbank manager',


)
