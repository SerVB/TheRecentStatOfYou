import json
import py_compile
import os
import shutil
import sys

REQUIRED_PYTHON_VERSION = "2.7.7"

print "Python version: " + sys.version
assert sys.version.find(REQUIRED_PYTHON_VERSION) == 0

config = json.load(open("build.json", "r"))

print "Remove %s dir" % config["buildRoot"]

if os.path.isdir(config["buildRoot"]):  # Remove build dir
    shutil.rmtree(config["buildRoot"])

for filePath in config["files"]:
    assert filePath[-3:] == ".py"

    sourceFileAbsolutePath = config["sourcesRoot"] + filePath
    destinationFileAbsolutePath = "build/res_mods/" + config["wotVersion"] + "/" + filePath + "c"
    destinationFileAbsoluteDir = destinationFileAbsolutePath[:destinationFileAbsolutePath.rfind("/")]

    if not os.path.isdir(destinationFileAbsoluteDir):
        os.makedirs(destinationFileAbsoluteDir)

    py_compile.compile(sourceFileAbsolutePath)
    sourceCompiledFileAbsolutePath = sourceFileAbsolutePath + "c"
    os.rename(sourceCompiledFileAbsolutePath, destinationFileAbsolutePath)

print "Files compiled: %d" % len(config["files"])
