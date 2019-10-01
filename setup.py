import os

from setuptools import setup


def read_dependencies(file_path):
    found_dependencies = []
    dir_name = os.path.dirname(file_path)

    with open(file_path) as requirements_file:
        for line in requirements_file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('#'):
                # comment
                continue

            elif line.startswith('-r'):
                nested_file = os.path.join(dir_name, line[2:].strip())
                found_dependencies.extend(read_dependencies(nested_file))
            else:
                found_dependencies.append(line)

    return found_dependencies


install_requires = read_dependencies('requirements.txt')

setup(
    name='currency_converter',
    version='',
    packages=['currency_converter'],
    url='',
    license='',
    author='iobukhov',
    author_email='proorc9@gmail.com',
    description='Currency Converter',
    install_requires=install_requires,
)
