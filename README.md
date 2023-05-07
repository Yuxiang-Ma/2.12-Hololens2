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
5. Open the scence. Go to "File"->"Open Scence", select the folder Scences/ and then select MainScene.unity. 

## Python

You may also need some Python packages to run the scripts. To handle dependencies, it is recommended to create a new conda environment (download Miniconda [here](https://docs.conda.io/en/latest/miniconda.html)), activate it, and then install the requirments.txt file:

```
conda create -n 2.120 python=3.9
conda activate 2.120
pip install -r requirements.txt
```

## Building and deploying 
Then you can build and deloy the project following the "Building and deploying" part of the [instructions](https://docs.google.com/document/d/17jsBMaB0MUb40jxV13PPMbnD3ZUolpd2wvhG_WX-qII/edit). 

When making the build, it is recommended by unity to specify an output directory for the build. (It is said that you might mess up the project by putting other folders in the unity project, including the build). The build takes a while, please be patient. 

## Communication Testing

## Usage

One simple test you can run is by navigating to the `Comms/Mock` folder and running the `mock_server.py` script on a server computer, and then running the `mock_hololens.py` script on a separate computer. Specifically, you may perform the following steps:

1. First obtain two laptops or computers to use, one to run the server code, and the other to run the mock client Python code.
2. On the client computer, edit the following line in `mock_hololens.py`:

```
# Replace the following with the IP address of the machine running the server
server_ip = "xx.xx.xx.xx"  # Define the server IP address (localhost in this case)
server_port = 21200  # Define the server port number
```

3. To find the server ip, open a terminal on the server computer and depending on your OS, run the following command:

```
# Windows
> ipconfig

# macOS / Linux
% ifconfig
```

4. Run the `mock_server.py` code on the server computer:

```
python mock_server.py
```

5. Run the `mock_hololens.py` on the client computer:

```
python mock_client.py
```

## Project Structure

## UI definition
### Buttons
| Button number     | Funtionality |
| ----------- | ----------- |
| 1           | Change IP of UR5       |
| 2           | Mobile Robot Overide       |
| 3           | Change IP of Mobile Robot |
| 4           | UR5 initialization and start/stop override|


