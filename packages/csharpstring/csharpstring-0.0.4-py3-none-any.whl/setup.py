from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "A String Package that emulates C# String manipulations."
LONG_DESCRIPTION = "A Package that emulates the C# String Class With all instance and static members."

setup(
	name="csharpstring",
	version=VERSION,
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	author="JSullivan",
	author_email="energy.keeper@gmail.com",
	license="MIT",
	packages=find_packages(),
	install_requires=[],
	keywords=['C#','CSharp', 'String'],
	classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
	]
)