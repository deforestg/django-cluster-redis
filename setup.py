from setuptools import find_packages, setup

setup(
    name='django-cluster-redis',
    version='1.0.5',
    description='django cluster redis',
    long_description='This is an AWS ElasticCache (or similar cluster) adapter for django redis',
    keywords='django cluster redis aws elasticcache',
    url='https://github.com/deforestg/django-cluster-redis',
    author='Gabriel de Forest',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'Django>=1.8.1',
        'django-redis>=4.7.0',
    ],
    include_package_data=True,
)
