from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tcw-tasks',
    version='0.1.4',
    author='J Leary',
    author_email='tinycontestwinners@gmail.com',
    description='contest cleanup script for tcw app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'tcw',
        'jinja2',
        'sendgrid',
    ],
    entry_points={
        'console_scripts': [
            'tcwinners = tcw_tasks.notify:main',
        ]
    }
)
