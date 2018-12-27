# Overview

This builds a C++ conan package:-

**Target Device:** Raspberry Pi (>=armv7)
**Library:** RF24
**Source:** https://github.com/nRF24/RF24

# Cross Compiling

## Pre-reqs 

A debian 9 system with: build-essential, docker, conan and cmake installed

## Pull Cross Compiler Image

```
docker run --rm dockcross/linux-armv7 > ./dockcross
./dockcross /bin/bash
```

## Add Conan Bintray Remote
```
conan user -p <APIKEY> -r iot <BINTRAY_USER>
conan remote add iot https://api.bintray.com/conan/<BINTRAY_USER>/cpp-rpi3 -i 0
```
## Compile and Upload
```
CONAN_PRINT_RUN_COMMANDS=1 conan create . conan/stable --build missing -s arch_build=armv7 -s arch=armv7
```
```
conan upload "*" -r iot --all -c
```

## Conanfile Reference
Given the remote is setup on the build host (as above), reference the library with:
```
RF24/1.3.1@conan/stable
```

