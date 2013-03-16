from setuptools import setup
import os

try:
    reqs = open(os.path.join(os.path.dirname(__file__),'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(name='django-feadme',
      version="2.0",
      description='',
      long_description="",
      author='Robert Weidlich',
      author_email='robert@fead.me',
      url='http://fead.me',
      packages=['feadme'],
      include_package_data=True,
      classifiers=[
          'Framework :: Django',
          ],
      )
