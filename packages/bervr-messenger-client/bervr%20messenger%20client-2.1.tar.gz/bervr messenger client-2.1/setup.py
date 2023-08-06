from setuptools import setup

setup(name="bervr messenger client",
      version="2.1",
      description="A client part for messenger",
      author="Aleksandr Filippov",
      author_email="bervrr@gmail.com",
      packages=["client"],
      install_requirements=['PyQt5', 'SQLAlchemy', 'pycryptodome', 'pycryptodomex']
      )
