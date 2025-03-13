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
            'inactive_user=blackduck_tools.scripts.inactive_user:main',
            'inactive_project_versions=blackduck_tools.scripts.inactive_project_versions:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Tools for managing inactive users and project versions in Blackduck hub',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/blackduck_tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
