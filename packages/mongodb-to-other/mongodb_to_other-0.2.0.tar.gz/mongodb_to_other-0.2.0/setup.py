
try:
    from setuptools import *
except ImportError:
    from distutils.core import *

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='mongodb_to_other',#包名
    version='0.2.0',#版本
    description="可以在flask中查看markdown代码",#包简介
    long_description=long_description,
    long_description_content_type="text/markdown",
  #读取文件中介绍包的详细内容
    include_package_data=True,#是否允许上传资源文件
    author='zyzlaozhang2011',#作者
    author_email='zyzlaozhang2011@163.com',#作者邮件
    maintainer='zyzlaozhang2011',#维护者
    maintainer_email='zyzlaozhang2011@163.com',#维护者邮件
    license='MIT License',#协议
    url='https://github.com/zyzlaozhang/mongodb_to_other',#github或者自己的网站地址
    packages=find_packages(),#包的目录
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',#设置编写时的python版本
],
    python_requires='>=3.7',#设置python版本要求
    install_requires=['pymongo',"xlwt","pymysql"],#安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },#设置命令行工具(可不使用就可以注释掉)
    
)

# import io
# import os
# import sys
# from shutil import rmtree

# from setuptools import find_packages, setup, Command

# # Package meta-data.
# NAME = 'mongodb_to_other'
# DESCRIPTION = '将mongodb导出为其他'
# URL = 'https://github.com/zyzlaozhang/mongodb_to_other'
# EMAIL = 'zyzlaozhang2011@163.com'
# AUTHOR = 'zyzlaozhang2011'
# REQUIRES_PYTHON = '>=3.6.0'
# VERSION = '0.1.4'

# # What packages are required for this module to be executed?
# REQUIRED = [
#     # 'requests', 'maya', 'records',
# ]

# # What packages are optional?
# EXTRAS = {
#     # 'fancy feature': ['django'],
# }

# # The rest you shouldn't have to touch too much :)
# # ------------------------------------------------
# # Except, perhaps the License and Trove Classifiers!
# # If you do change the License, remember to change the Trove Classifier for that!

# here = os.path.abspath(os.path.dirname(__file__))

# # Import the README and use it as the long-description.
# # Note: this will only work if 'README.md' is present in your MANIFEST.in file!
# try:
#     with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#         long_description = '\n' + f.read()
# except FileNotFoundError:
#     long_description = DESCRIPTION

# # Load the package's __version__.py module as a dictionary.
# about = {}
# if not VERSION:
#     project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
#     with open(os.path.join(here, project_slug, '__version__.py')) as f:
#         exec(f.read(), about)
# else:
#     about['__version__'] = VERSION


# class UploadCommand(Command):
#     """Support setup.py upload."""

#     description = 'Build and publish the package.'
#     user_options = []

#     @staticmethod
#     def status(s):
#         """Prints things in bold."""
#         print('\033[1m{0}\033[0m'.format(s))

#     def initialize_options(self):
#         pass

#     def finalize_options(self):
#         pass

#     def run(self):
#         try:
#             self.status('Removing previous builds…')
#             rmtree(os.path.join(here, 'dist'))
#         except OSError:
#             pass

#         self.status('Building Source and Wheel (universal) distribution…')
#         os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

#         self.status('Uploading the package to PyPI via Twine…')
#         os.system('twine upload dist/*')

#         self.status('Pushing git tags…')
#         os.system('git tag v{0}'.format(about['__version__']))
#         os.system('git push --tags')

#         sys.exit()


# # Where the magic happens:
# setup(
#     name=NAME,
#     version=about['__version__'],
#     description=DESCRIPTION,
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     author=AUTHOR,
#     author_email=EMAIL,
#     python_requires=REQUIRES_PYTHON,
#     url=URL,
#     packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
#     # If your package is a single module, use this instead of 'packages':
#     # py_modules=['mypackage'],

#     # entry_points={
#     #     'console_scripts': ['mycli=mymodule:cli'],
#     # },
#     install_requires=REQUIRED,
#     extras_require=EXTRAS,
#     include_package_data=True,
#     license='MIT',

#     classifiers=[
#         # Trove classifiers
#         # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: Implementation :: CPython',
#         'Programming Language :: Python :: Implementation :: PyPy'
#     ],
#     # $ setup.py publish support.
#     cmdclass={
#         'upload': UploadCommand,
#     },
# )