from setuptools import setup, find_packages

setup(
    name='blackduck_tools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'inactive_user=hub-scripts.scripts.inactive_user:main',
            'inactive_project_versions=hub-scripts.scripts.inactive_project_versions:main',
        ],
    },
    author='Dylan',
    author_email='dylanm@blackduck.com,
    description='Tools for managing inactive users and project versions in Blackduck hub',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dc-moses/hub-scripts',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
