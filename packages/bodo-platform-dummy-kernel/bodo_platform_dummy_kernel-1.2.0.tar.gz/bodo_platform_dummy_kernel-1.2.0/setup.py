import setuptools
import versioneer

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")

setuptools.setup(
    name="bodo_platform_dummy_kernel",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A simple wrapper around IPython Kernel for the Bodo Platform Notebook",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Bodo-inc/bodo-platform-dummy-kernel",
    packages=setuptools.find_packages(),
    author="Bodo, Inc.",
    author_email="noreply@bodo.ai",
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
)
