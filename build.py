import json
import py_compile
import os
import shutil
import sys
import zipfile

REQUIRED_PYTHON_VERSION = "2.7.7"

print "Python version: " + sys.version
assert sys.version.find(REQUIRED_PYTHON_VERSION) == 0

config = json.load(open("build.json", "r"))

print "Remove %s dir" % config["buildRoot"]

if os.path.isdir(config["buildRoot"]):  # Remove build dir
    shutil.rmtree(config["buildRoot"])
os.makedirs(config["buildRoot"])

packagedFilePath = config["buildRoot"] + config["packageName"] + "_" + str(config["modVersion"]) + ".wotmod"

with zipfile.ZipFile(packagedFilePath, "w", zipfile.ZIP_STORED) as packagedFile:
    for filePath in config["files"]:
        assert filePath[-3:] == ".py"

        sourceFileAbsolutePath = config["sourcesRoot"] + filePath
        py_compile.compile(sourceFileAbsolutePath)

        destinationFilePackagePath = "res/" + filePath + "c"
        sourceCompiledFileAbsolutePath = sourceFileAbsolutePath + "c"
        packagedFile.write(sourceCompiledFileAbsolutePath, arcname=destinationFilePackagePath)
        os.remove(sourceCompiledFileAbsolutePath)

print "Files compiled: %d" % len(config["files"])
print "Package compiled: %s" % packagedFilePath
