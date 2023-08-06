from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='discordpresence',
    version='1.0.0',
    description='Package to set discord presnece.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='sscefalix',
    author_email='dimabykov189@gmail.com',
    keywords=['Discord', 'DiscordPresence', 'Presence'],
    url='https://github.com/sscefalix/discordpresence',
    download_url='https://pypi.org/project/discordpresence/',
    python_requires='>=3.8'
)

install_requires = [
    'pypresence>=4.2.1'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)