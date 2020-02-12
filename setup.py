import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'waitress',
    'pyramid-chameleon',
    'psycopg2',
    'alembic',
    'zope.sqlalchemy',
    'pyramid-tm'
    ]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'mockito',
    'sqlalchemy'
]

setup(name='referral_program',
      version='0.0.1',
      description='Quick Demo of a Referral Program API',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Renier Venter',
      author_email='renierventer@protonmail.com',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
        'dev': dev_requires,
      },
      entry_points="""\
      [paste.app_factory]
      main = referral_program:main
      """,
      )
