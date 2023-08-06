from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
      name="radicale_ldap_auth",
      packages=["radicale_ldap_auth"],
      version="0.0.3",
      author="Viktor Gorinskiy",
      author_email="viktor@gorinskiy.ru",
      description="Плагин авторизации в radicale под доменными пользователями",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/viktor-gorinskiy/radicale_ldap_auth",
	install_requires=[
            'pyasn1==0.4.8',
            'pyasn1-modules==0.2.8',
            'python-ldap==3.4.3'
      ],
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
      )