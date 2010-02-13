#!/usr/bin/env python

import os
import re
import sys

# the build script lives below
sys.path.append("../..")
from pybake import *

# this is really good bit...
if sys.platform == 'linux2':
    CC = "gcc"
    OBJECT_SUFFIX = ".o"
    compile_args = lambda ts, ds: [CC, "-c", "-o", ts[0], ds[0], "-g", "-Wall"]
    link_args = lambda ts, ds: [CC, "-o", ts[0]] + ds + ["-g", "-Wall"]
elif sys.platform == 'win32':
    # the PATH variable does not comtain the MSVC environment under windows,
    # and we somehow need to get it into our child processes.
    # running this .bat file "%VS90COMNTOOLS%"vsvars32.bat, sets up the environment,
    # but how can we do this before the build script is started?
    CC = "cl"
    OBJECT_SUFFIX = ".obj"
    compile_args = lambda ts, ds: [CC, "/c", "/Fo"+ts[0], ds[0], "/nologo"]
    # cl translates to link's even more bizarre parameters for us
    link_args = lambda ts, ds: [CC, "/Fe"+ts[0], "/nologo"] + ds
else:
    # if you are a developer using a mac, seek professional help
    assert False

OBJECTS = map(lambda o: o + OBJECT_SUFFIX, "demo_a demo_b".split())
# how to build .o files from .c files

ImplicitRule(r".*" + re.escape(OBJECT_SUFFIX) + r"$",
            BuildStep(compile_args),
            lambda x: ([x], [re.sub(re.escape(OBJECT_SUFFIX) + r"$", ".c", x)]))
# how to build, and what our binary depends on
binary = ExplicitRule(["demo.exe"], OBJECTS, BuildStep(link_args))

# update the binary!
binary.update_all()
