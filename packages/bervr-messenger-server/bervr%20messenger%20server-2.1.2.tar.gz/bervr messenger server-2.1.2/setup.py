from setuptools import find_packages, setup

setup(name="bervr messenger server",
      version="2.1.2",
      description="A server part for messenger",
      author="Aleksandr Filippov",
      author_email="bervrr@gmail.com",
      packages=find_packages(),
      install_requirements=['PyQt5', 'SQLAlchemy', 'pycryptodome', 'pycryptodomex', 'cahrdet']
      )
