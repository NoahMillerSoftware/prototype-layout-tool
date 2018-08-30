import os
from distutils.core import setup

# get __version__ from plt package
exec(open(os.path.join('prototype_layout_tool', 'version.py')).read())

setup(
    name='prototype_layout_tool',
    version=__version__,
    packages=['prototype_layout_tool',],
    scripts=[os.path.join('scripts', 'plt.py'),],
    long_description=open('README.md').read(),
    author='Noah Miller',
    author_email='noah.miller@gmail.com',
    install_requires=['reportlab',],
)
