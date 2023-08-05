import setuptools

with open("Readme.MD", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="arch_gen",
    version="0.0.1",
    author="Arch Reactor",
    author_email="nobody@nobody.com",
    packages=["arch_gen"],
    description="A sample test package",
    long_description="testing",
    long_description_content_type="text/markdown",
    url="https://bitbucket.trimble.tools/users/aravinth_karthikeyan_trimble.com/repos/javacodex/arch-reactor/",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)
