from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment, RunEnvironment

# Python 3
#import ConfigParser
#import urllib.request

import configparser 
import urllib2

source_repo = "nRF24/RF24"
git_source_repo = "https://github.com/" + source_repo
raw_source_repo = "https://raw.githubusercontent.com/" + source_repo + "/master"

def parse_library_properties():
	
    url = raw_source_repo + "/library.properties"
    print("INFO: url: " + url)
    contents = urllib2.urlopen(url).read()
       
    config = configparser.ConfigParser(strict=False)
    config.read_string(u"[DEFAULT]\n" + contents)
       
    return config["DEFAULT"]

library_properties = parse_library_properties()

conan_version = library_properties["version"]

print("INFO: Version from git repo: " + conan_version)

class Rf24Conan(ConanFile):
    name = "RF24"
    version = conan_version
    license = "GPL v2.0"
    url = "https://github.com/steve-white/cpp-rpi3"
    description = library_properties["sentence"]
    topics = ("RF24", "Raspberry Pi", "armv7")
    settings = { "arch" : "armv7", "arch_build" : "armv7" }
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone " + git_source_repo + " .")
        self.run("git checkout master")
    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("echo $LD_LIBRARY_PATH , $CFLAGS , $LDFLAGS , $CPPFLAGS")
            self.run("./configure --driver=SPIDEV --soc=BCM2837 --extra-cflags=\"$CFLAGS $CPPFLAGS\"") # --extra-ldflags=\"$LDFLAGS\"
            self.run("make")
 
    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    #def package_info(self):
        #self.cpp_info.libs = ["rf24"]

