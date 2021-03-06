from setuptools import setup, find_packages
from helga_youtube_meta import __version__ as version


setup(
    name='helga-youtube-meta',
    version=version,
    description=('Provide information for youtube related metadata'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat :: Internet Relay Chat'],
    keywords='irc bot youtube-meta',
    author='Jon Robison',
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/helga-youtube-metadata',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['helga_youtube_meta.plugin'],
    zip_safe=True,
    install_requires=[
        'helga',
        'python-dateutil',
        'requests',
    ],
    test_suite='',
    entry_points=dict(
        helga_plugins=[
            'youtube-meta = helga_youtube_meta.plugin:youtube_meta',
        ],
    ),
)
