import setuptools

VERSION = '0.0.1'
DESCRIPTION = 'Light-weight CLI tool for yoake.moe'

setuptools.setup(
    name="yoakecli",
    version=VERSION,
    author="Yoake",
    author_email="zedovblack@gmail.com",
    description=DESCRIPTION,
    long_description="What did you expect? A long description? Nah",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Android",
        "Natural Language :: Vietnamese"
    ],
    entry_points={
        'console_scripts': [
            'yoakecli = yoakecli.yoakeCLI:main',
            'ycli = yoakecli.yoakeCLI:main'
        ]
    }
)