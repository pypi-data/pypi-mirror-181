from setuptools import setup, find_packages


setup(
    name="deskpanel",
    version="0.1.0",
    license="MIT",
    author="Oleh Dzoba",
    packages=find_packages(),
    url="https://github.com/olehdzoba/deskpanel",
    keywords=["python", "windows", "desktop", "panel", "wallpaper"],
    install_requires=[
        "Pillow==9.3.0",
        "pywin32==305",
        "screeninfo==0.8.1"
      ],
)