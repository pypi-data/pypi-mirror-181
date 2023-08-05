#!/usr/bin/env python
#
# Enable cython support for slightly faster eval scripts:
# python -m pip install cython numpy
# CYTHONIZE_EVAL= python setup.py build_ext --inplace
#
# For MacOS X you may have to export the numpy headers in CFLAGS
# export CFLAGS="-I /usr/local/lib/python3.6/site-packages/numpy/core/include $CFLAGS"

import os
import glob
import platform
from vspscripts import __version__
from setuptools import setup, Extension, find_packages

def get_extensions():
    extensions_dir = os.path.join(os.path.dirname(__file__), 'vspscripts', 'alignment')
 
    main_file = glob.glob(os.path.join(extensions_dir, "*.cpp"))
    source = glob.glob(os.path.join(extensions_dir, "Clibrary", "src", "*.cpp"))
 
    sources = main_file + source

    # sources = [os.path.join(extensions_dir, s) for s in sources]

    # print(sources)

    include_dirs = [
        "/usr/include",
        "/usr/local/include/opencv4",
        os.path.join(extensions_dir, "Clibrary", "include")
    ]
 
    ext_modules = [
        Extension(
            "vspscripts/alignment/cModPyAlignment",
            sources=sources,
            include_dirs=include_dirs,
            libraries=['opencv_core', 'opencv_highgui', 'opencv_imgproc', 'opencv_imgcodecs', 'python3.6m'],
            # library_dirs=['/usr/local/lib64'],
            # extra_objects=[]
        )
    ]
 
    return ext_modules

include_dirs = []
ext_modules = []
if 'CYTHONIZE_EVAL' in os.environ:
    from Cython.Build import cythonize
    import numpy as np
    include_dirs = [np.get_include()]

    os.environ["CC"] = "g++"
    os.environ["CXX"] = "g++"

    pyxFile = os.path.join("vspscripts",
                           "evaluation", "addToConfusionMatrix.pyx")
    ext_modules = cythonize(pyxFile)

if platform.system() == 'Linux':
    ext_modules = ext_modules + get_extensions()

with open("README.md") as f:
    readme = f.read()

# with open(os.path.join('vspscripts', 'VERSION')) as f:
#     version = f.read().strip()

console_scripts = [
    'csEvalPixelLevelSemanticLabeling = vspscripts.evaluation.evalPixelLevelSemanticLabeling:main',
    'csEvalInstanceLevelSemanticLabeling = vspscripts.evaluation.evalInstanceLevelSemanticLabeling:main',
    'csEvalPanopticSemanticLabeling = vspscripts.evaluation.evalPanopticSemanticLabeling:main',
    'csEvalObjectDetection3d = vspscripts.evaluation.evalObjectDetection3d:main',
    'csCreateTrainIdLabelImgs = vspscripts.preparation.createTrainIdLabelImgs:main',
    'csCreateTrainIdInstanceImgs = vspscripts.preparation.createTrainIdInstanceImgs:main',
    'csCreatePanopticImgs = vspscripts.preparation.createPanopticImgs:main',
    'csDownload = vspscripts.download.downloader:main',
    'csPlot3dDetectionResults = vspscripts.evaluation.plot3dResults:main'
]

gui_scripts = [
    'csViewer = vspscripts.viewer.cityscapesViewer:main [gui]',
    'csLabelTool = vspscripts.annotation.cityscapesLabelTool:main [gui]'
]

config = {
    'name': 'vspscripts',
    'description': 'Scripts for the VSP Dataset',
    'long_description': readme,
    'long_description_content_type': "text/markdown",
    'author': 'WJG',
    'url': '',
    'author_email': 'wangjiangong2018@ia.ac.cn',
    'license': 'MIT license',
    'version': __version__,
    'install_requires': ['numpy', 'matplotlib', 'pillow', 'appdirs', 'pyquaternion', 'coloredlogs', 'tqdm', 'typing'],
    'setup_requires': ['setuptools>=18.0'],
    'extras_require': {
        'gui': ['PyQt5']
    },
    'packages': find_packages(),
    'scripts': [],
    'entry_points': {'gui_scripts': gui_scripts,
                     'console_scripts': console_scripts},
    'include_package_data': False,
    'package_data': {'': ['VERSION', 'icons/*.png']},
    'ext_modules': ext_modules,
    'include_dirs': include_dirs
}

setup(**config)
