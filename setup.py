from setuptools import setup, find_packages

setup(
    name='django-feedparser',
    version=__import__('django_feedparser').__version__,
    description=__import__('django_feedparser').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='dthenon@emencia.com',
    url='https://github.com/sveetch/django-feedparser',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'requests>=2.7.0',
        'feedparser>=5.1.3',
    ],
    include_package_data=True,
    zip_safe=False
)
