from setuptools import setup

setup(name="bervr messenger server",
      version="2.1.1",
      description="A server part for messenger",
      author="Aleksandr Filippov",
      author_email="bervrr@gmail.com",
      packages=["server", "server.server"],
      package_dir={
          "": ".",
          "server": "./server",
      },
      install_requirements=['PyQt5', 'SQLAlchemy', 'pycryptodome', 'pycryptodomex']
      )
