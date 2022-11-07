import setuptools

with open("README.md ","r") as file:
	long_des=file.read()

setuptools.setup(
	name="preprocess_ady",
	version="0.0.1",
	author="Adyansh Das",
	author_mail="adyanshdas1@gmail.com",
	description="This is a preprocessing package",
	long_description= long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
	'Programming Language" :: Python ::3',
	'License :: OSI Approved :: MIT License',
	'Operating System :: OS Independent'],
	python_requires='>=3.5'





	)