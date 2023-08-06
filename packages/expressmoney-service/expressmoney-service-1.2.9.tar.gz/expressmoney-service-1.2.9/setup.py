"""
py setup.py sdist
twine upload dist/expressmoney-service-1.2.9.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney-service',
    packages=setuptools.find_packages(),
    version='1.2.9',
    description='Remote services',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('expressmoney', 'django-phonenumber-field[phonenumberslite]'),
    python_requires='>=3.7',
)
