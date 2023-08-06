from setuptools import setup, find_packages

# load the project description

with open('README.md', 'r') as fh:

    ld = fh.read()

# set up the pip pkg installer

setup(name = 'tnmake', # Thumbnail!MAKER
    version = '0.2.0',
    license = 'GPLv3+',
    description = 'Thumbnail!MAKER creates customisable thumbnails',
    package_dir = {'':'src'},
    packages = find_packages(where='src'),
    install_requires = ['python-iso639', 'python-rapidjson>=1.6'],
    author = 'nschepsen',
    author_email = 'nikolaj@schepsen.eu',
    # github
    keywords = 'library, video, tools',
    # module's metadata
    entry_points = {
        'console_scripts': ['tnmake=tnmake.main:main']},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Video', 'Topic :: Utilities'
        ],
    long_description = ld, # long description
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/nschepsen/thumbnail-maker' # repo
)

# Thumbnail!MAKER creates customisable thumbnails (ffmpeg wrapper)