from setuptools import setup, find_packages

setup(name="bervr messenger client",
      version="2.1.3",
      description="A client part for messenger",
      author="Aleksandr Filippov",
      author_email="bervrr@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'SQLAlchemy', 'pycryptodome', 'pycryptodomex', 'cahrdet'],
      scripts=['./client/client_run.py']
      )
