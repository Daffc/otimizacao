import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read()

setuptools.setup(
    name="bb-caminhada",
    version="0.0.1",
    author="Douglas Affonso Clementino",
    author_email="douglas.affc@gmail.com",
    description="Programa para encontrar pelo metodo Branch and Bound ciclo simples cuja somatória das arestas é maximal a partir de um vertice.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["bb-caminhada=bb_caminhada:main"]},
    python_requires='>=3.6',
)