import os

from setuptools import setup, find_packages


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


test_requirements = read_dependencies('requirements/requirements-test.txt')
develop_requirements = read_dependencies('requirements/requirements-dev.txt')
install_requires = read_dependencies('requirements/requirements-prod.txt')
setup_requires = read_dependencies('requirements/requirements-setup.txt')

setup(
    name='currency_converter',
    version='',
    packages=find_packages(
        exclude=('tests',),
        include=('currency_converter', 'currency_converter.*'),
    ),
    url='',
    license='',
    author='Ilia Obukhov',
    author_email='proorc9@gmail.com',
    description='Currency Converter',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=test_requirements,
)
