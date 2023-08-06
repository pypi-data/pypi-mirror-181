import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='nsg-python-sdk',
                 version='0.0.3',
                 description='NetSpyGlass SDK',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 classifiers=[
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
                 ],
                 url='https://github.com/happygears/nsg-python-sdk',
                 author='Happy Gears, Inc',
                 license='Apache',
                 install_requires=[
                     'ipaddr', 'protobuf', 'click', 'sortedcontainers'],
                 py_modules=['nsg', 'ipaddr', 'serialization', 'tag_selector', 'view'],
                 entry_points={
                     'console_scripts': [
                         'nsgsdk=bin.nsgsdk:process_request',  # command=package.module:function
                     ],
                 },
                 packages=setuptools.find_packages(),
                 python_requires='>=3.6')
