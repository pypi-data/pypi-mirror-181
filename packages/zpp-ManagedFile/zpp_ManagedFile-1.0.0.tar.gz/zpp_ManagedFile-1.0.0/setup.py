from setuptools import setup
import os
import zpp_ManagedFile

setup(name="zpp_ManagedFile",
      version=zpp_ManagedFile.__version__,
      author="ZephyrOff",
      author_email="contact@apajak.fr",
      keywords = "file zephyroff",
      classifiers = ["Development Status :: 5 - Production/Stable", "Environment :: Console", "License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3"],
      packages=["zpp_ManagedFile"],
      description=zpp_ManagedFile.__descriptor__,
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      long_description_content_type='text/markdown',
      url = "https://github.com/ZephyrOff/py-zpp_ManagedFile",
      platforms = "ALL",
      license="MIT")