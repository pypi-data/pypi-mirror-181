# Change version & download_url in setup.py
# Run `python3 setup.py sdist`
# Create new py3 env and install contents of dist/ manually from pip `pip install ~/proj/dist/filename.tar.gz` and test it.
# Push the changes
# Create new release on GitHub
# Activate py env
# pip install twine
# twine upload --repository Convert2PDF dist/*


# from distutils.core import setup
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'Convert2PDF',         # How you named your package folder (MyLib)
  packages = ['Convert2PDF'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  download_url = 'https://github.com/ashfaque/Convert2PDF/archive/refs/tags/v_01.tar.gz',    # Link of your source code
  license='GNU GPLv3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository or, https://choosealicense.com/
  description = 'Convert from different file formats to PDF format.',   # Give a short description about your library
  long_description_content_type = "text/markdown",    # Really important if you are using README.md format.
  long_description = long_description,      # Long description read from the the readme file
  author = 'Ashfaque Alam',                   # Type in your name
  author_email = 'ashfaquealam496@yahoo.com',      # Type in your E-Mail
  url = 'https://github.com/ashfaque/Convert2PDF',   # Provide either the link to your github or to your website
  keywords = ['ASHFAQUE', 'ASHFAQUE ALAM', 'CONVERT', 'PDF', 'CONVERT TO PDF'],   # Keywords that define your package best
  install_requires=[            # Your packages dependencies
          'img2pdf'
          , 'Pillow'
          , 'fpdf'
          , 'PyPDF2'
          ,
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)