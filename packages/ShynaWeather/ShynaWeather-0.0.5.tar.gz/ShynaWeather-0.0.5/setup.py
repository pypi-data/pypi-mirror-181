from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
     name='ShynaWeather',
     version='0.0.05',
     packages=find_packages(),
     author="Shivam Sharma",
     author_email="shivamsharma1913@gmail.com",
     description="This package will take care of maintaining the Weather details as per my last location.",
     long_description=long_description,
     long_description_content_type="text/markdown",
    )

install_requires = ['ShynaDatabase', 'ShynaTime', 'requests', 'setuptools', 'wheel']

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
