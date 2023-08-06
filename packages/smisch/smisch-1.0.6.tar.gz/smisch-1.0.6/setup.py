from setuptools import setup, find_packages

setup(
    name='smisch',  # názov knižnice
    version='1.0.6',  # verzia knižnice
    packages=find_packages(),  # nájde všetky balíčky v adresári
    py_modules=['smisch',
    'src.print.anim_print'],  # názov súboru s funkciami
    install_requires=[],
    author='Smisch',  # meno autora
    author_email='smisch@smisch.sk',  # email autora
    description='Neviem',  # stručný popis knižnice
    license='MIT',  # licencia knižnice
    keywords='print input',  # kľúčové slová
)