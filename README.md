# 2.12-Hololens Repo 

# Description 
This repo is based on [2.120-Starter](https://drive.google.com/drive/folders/1VxoxGX22adgEMrdXR7cvyz42zqQqDNdy) code. But you do not need that whole package, and that will not work because you will have to rebuild some folders and files after moving the unity project. [Here](https://gamedevbeginner.com/how-to-move-or-copy-a-unity-project-without-breaking-it/) is an instruction about how to move a unity project safely. 

So intead of using [2.120-Starter](https://drive.google.com/drive/folders/1VxoxGX22adgEMrdXR7cvyz42zqQqDNdy) code, you can follow the instructions below to build the project.

# Installation 
## Getting started 
1. Install Unity Hub and from there install Unity 2021.3.22f1. 
2. Install Visual Studio 2022 and its necessary components following [the official guide](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/install-the-tools). Make sure you install all the components for hololens2. 
3. Pull this repo with `git clone git@github.com:Yuxiang-Ma/2.12-Hololens2.git`. 
4. Launch Unity Hub, import the project (“Open -> Add project from disk”), and launch Unity. 

## Building and deploying 
Then you can build and deloy the project following the "Building and deploying" part of the [instructions](https://docs.google.com/document/d/17jsBMaB0MUb40jxV13PPMbnD3ZUolpd2wvhG_WX-qII/edit). 
When making the build, it is recommended by unity to specify an output directory for the build. (It is said that you might mess up the project by putting other folders in the unity project, including the build). The build takes a while, please be patient. 
