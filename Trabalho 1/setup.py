import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read()

setuptools.setup(
    name="lp-tempo",
    version="0.0.1",
    author="Douglas Affonso Clementino",
    author_email="douglas.affc@gmail.com",
    description="Programa para escalonamento de tarefas por máquinas utilizando de programação linear",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["lp-tempo=lp_tempo:main"]},
    python_requires='>=3.6',
)