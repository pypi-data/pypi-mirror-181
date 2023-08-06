from setuptools import setup, find_packages

setup(
    name='smischlib',  # názov knižnice
    version='1.0.5',  # verzia knižnice
    packages=find_packages(),  # nájde všetky balíčky v adresári
    py_modules=['smischlib',
    'src.utilities.running_os',
    'src.console.clear_console',
    'src.input.anim_input',
    'src.utilities.running_os',
    'src.print.anim_print',
    'src.input.ask_input'],  # názov súboru s funkciami
    install_requires=[],
    author='Smisch',  # meno autora
    author_email='smisch@smisch.sk',  # email autora
    description='Library with addon functions for python.',  # stručný popis knižnice
    license='MIT',  # licencia knižnice
    keywords='print input',  # kľúčové slová
)