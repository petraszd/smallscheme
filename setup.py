from distutils.core import setup

setup(
    name="smallscheme",
    description="scheme interpreter written in python",
    author="Petras Zdanavicius",
    author_email="petraszd@gmail.com",
    url="http://bitbucket.org/petraszd/smallscheme/",
    version="0.1",
    packages=['smallscheme'],
    package_data={'smallscheme': ["smallscheme/*"]},
    scripts = ["run-smallscheme"],
    license="MIT",
)

