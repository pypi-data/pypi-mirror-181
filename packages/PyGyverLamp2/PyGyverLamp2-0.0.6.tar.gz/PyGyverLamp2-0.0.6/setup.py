import setuptools

description = 'Python module for control GyverLamp2'

setuptools.setup(
    name="PyGyverLamp2",
    version="0.0.6",
    author="KirillMonster",
    author_email="k1rill_monster@mail.ru",
    packages=["PyGyverLamp2"],
    description=description,
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/KirillMonster/PyGyverLamp2",
    license='MIT',
    python_requires='>=3.9',
    install_requires=['flask']
)
