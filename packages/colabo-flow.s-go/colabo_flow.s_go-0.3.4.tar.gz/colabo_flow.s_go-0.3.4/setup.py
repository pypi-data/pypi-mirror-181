import sys
from setuptools import setup, find_packages
import json

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
print(f"this_directory: {this_directory}")

import sys
setup_command: str = sys.argv[1]
print(f"setup_command: {setup_command}")

is_build = setup_command.lower() == "sdist"
is_install = not is_build

is_python3 = sys.version_info >= (3, 0)
is_python2 = not is_python3

print(f"is_build: {is_build}, is_install: {is_install}, is_python2: {is_python2}, is_python3: {is_python3}, ")

# Load the `README.md` file
readme_path = path.join(this_directory, 'README.md')

# python3
if is_python3:
	# https://docs.python.org/3/library/functions.html#open
	with open(readme_path, encoding='utf-8') as f:
		long_description = f.read()
# python2
else:
	# https://docs.python.org/2/library/functions.html#open
	with open(readme_path) as f:
		long_description = f.read()

# import shutil
# valid for building package
package_path_build = path.join(this_directory, '../package.json')

built_info_path =  path.join(this_directory, 'built_info.json')

if is_build:
	# building (`setup.py sdist`)

	# loading `../package.json`
	try:
		print(f"[BUILDING] package package_path_build: {package_path_build}")
		# python3
		if is_python3:
			with open(package_path_build, encoding='utf-8') as f:
				package_json_str = f.read()
		# python2
		else:
			with open(package_path_build) as f:
				package_json_str = f.read()
		print(f"[BUILDING] succeeded: package package_path_build: {package_path_build}")
		# shutil.copyfile(package_path_build, package_path_install)
	except (FileNotFoundError):
		# failed
		print(f"[BUILDING] FAILED: package package_path_build: {package_path_build}")


	# extract version and name from the `package.json`

	package_json = json.loads(package_json_str)

	# extract and fix version
	package_version = package_json['version']
	package_version = f"{package_version}"
	# package_version = "0.2.11.1"
	print(f"package_version: {package_json['version']} -> {package_version}")

	# extract and fix package name
	package_name = package_json['name']
	package_name = package_name.replace('@', '')
	package_name = package_name.replace('-', '_')
	package_name = package_name.replace('/', '.')
	# package_name = "colabo_flow.s_go"
	print(f"package_name: '{package_json['name']}' => '{package_name}'")


	package_requirements_list = []
	# https://pypi.org/project/requirements-parser/
	import requirements
	# extract requirements for the `install_requires` from the `requirements.txt` file
	with open('requirements.txt', 'r') as fd:
			for req in requirements.parse(fd):
				print(req.name, req.specs)
				package_requirements_list.append(f"{req.name}{req.specs[0][0]}{req.specs[0][1]}")
	print(f"package_requirements_list: {package_requirements_list}")

	# # adding `setup()` required packages
	# package_requirements_list.append("requirements")
	# print(f"package_requirements_list with the `setup()` required packages: {package_requirements_list}")

	built_info_data = {
		"name": package_name,
		"version": package_version,
		"requirements_list": package_requirements_list,
	}
	if is_python3:
		with open(built_info_path, 'w', encoding='utf-8') as f:
			json.dump(built_info_data, f, ensure_ascii=False, indent=4)
	else:
		with open(built_info_path, 'w') as f:
			json.dump(built_info_data, f)

else:
	# installing (`setup.py egg_info`)
	try:
		print(f"[INSTALLING] package built_info_path: {built_info_path}")
		# python3
		if is_python3:
			with open(built_info_path, encoding='utf-8') as f:
				built_info_data_str = f.read()
		# python2
		else:
			with open(built_info_path) as f:
				built_info_data_str = f.read()
		print(f"[INSTALLING] succeeded: package built_info_path: {built_info_path}")
	except (FileNotFoundError):
		# failed
		print(f"[INSTALLING] FAILED: package built_info_path: {built_info_path}")

	built_info_data = json.loads(built_info_data_str)
	package_name = built_info_data["name"]
	package_version = built_info_data["version"]
	# IMPORTANT: if you are on the test PiPy (TestPyPI) like this one https://test.pypi.org/project/colabo-flow-s-go/0.2.11.post1/
	# the requirements will NOT be satisfied as they are usually do not exist on the test PiPy or at least not with exact version you might required (copy from requirements.)

	package_requirements_list = built_info_data["requirements_list"]
	print(f"package_name: {package_name}, package_version: {package_version}, package_requirements_list: {package_requirements_list}")

setup(
	name=package_name,
	# other arguments omitted
	long_description=long_description,
	long_description_content_type='text/markdown',
	version=package_version,
	url='https://github.com/Cha-OS/',
	# download_url,
	project_urls={
		'website': 'http://colabo.space',
		'organization': 'http://cha-os.org'
	},
	author='ChaOS',
	author_email='chaos.ngo@gmail.com',
	license='MIT',
	description='A python ColaboFlow.Go (CF.Go) puzzle for supporting execution of workflow tasks over the RabbitMQ broker',
	keywords=['colabo','RabbitMQ','flow','colaboflow', 'go', 'process', 'workflow'],

	# implicit, regular structure
	# packages=find_packages(),
	# explicit, advanced use cases
	packages=["colabo_flow.s_go"],

	# requires=['grpcio', 'googleapis-common-protos', 'python-dateutil'],

	# programmatically importing and using external `requirements.txt` as
	# the requirements from `requirements.txt` are not automatically loaded and installed
	# https://setuptools.pypa.io/en/latest/userguide/dependency_management.html
	# IMPORTANT: if you are on the test PiPy (TestPyPI) like this one https://test.pypi.org/project/colabo-flow-s-go/0.2.11.post1/
	# the requirements will NOT be satisfied as they are usually do not exist on the test PiPy or at least not with exact version you might required (copy from requirements.)
	install_requires=package_requirements_list,

	# Adding non-python files to the package
	# https://stackoverflow.com/a/46320769/257561
	# this doesn't work we use `MANIFEST.in` instead
	include_package_data=True,
	package_data={'': ['package.json']},

	# https://setuptools.pypa.io/en/latest/deprecated/zip_safe.html
	zip_safe=False,
)
