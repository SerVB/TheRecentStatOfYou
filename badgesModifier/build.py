# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html
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

packagedFilePath = config["buildRoot"] + config["packageName"] + "_" + config["wotVersion"] + "-" + str(config["modVersion"]) + ".wotmod"

with zipfile.ZipFile(packagedFilePath, "w", zipfile.ZIP_STORED) as packagedFile:
    for pyFilePath in config["filesToCompile"]:
        assert pyFilePath[-3:] == ".py"

        pyFileAbsolutePath = config["sourcesRoot"] + pyFilePath
        py_compile.compile(pyFileAbsolutePath)

        destinationFilePackagePath = "res/" + pyFilePath + "c"
        sourceCompiledFileAbsolutePath = pyFileAbsolutePath + "c"
        packagedFile.write(sourceCompiledFileAbsolutePath, arcname=destinationFilePackagePath)
        os.remove(sourceCompiledFileAbsolutePath)

    for filePath in config["filesToCopy"]:
        fileAbsolutePath = config["sourcesRoot"] + filePath
        destinationFilePackagePath = "res/" + filePath
        packagedFile.write(fileAbsolutePath, arcname=destinationFilePackagePath)

print "Files compiled: %d" % len(config["filesToCompile"])
print "Files copied: %d" % len(config["filesToCopy"])
print "Package compiled: %s" % packagedFilePath
