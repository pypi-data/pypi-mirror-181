import setuptools

with open("./README.rst",'r') as f:
	data= f.read()
setuptools.setup(name='traffic_forward',
      version='1.0.0',
      description='This tool is used for forwarding local and remote (intranet) traffic',
      long_description=data,
      url='https://github.com/doudoudedi/traffic_forward',
      author='doudoudedi',
      author_email='doudoudedi233@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      entry_points={
      'console_scripts': [
      'traffic_forward = traffic_forward:main',
    ]
  }
)

