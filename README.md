# Title: Environmental Variables and Production Pipeline
This project integrates environmental variables, Gitbash Pipeline helpers, and Maya Python Scripting to build a simple yet effective production workflow. 
If run in maya script editor it will generate a UI window with buttons that create shapes and buttons that augment shaders, similiar to the previous assignment3. 
Conversely if run in Gitbash it will support environment variables (PROJECT, SHOT, TASK, PROJECT_DIR) when run through mayapy. Command line arguments (--create,--color,--save) for automated batch processes have been worked in. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation
 1. Clone or download the project folder from Gitbash
 2. add the .sh pipeline assistant 
   Inside pipeline-aliases.sh, define:
	export PROJECT_ROOT="$HOME/shows" 
        project(){
          export PROJECT=$1
          }
        shot(){
         export SHOT="$1"
         export TASK="$2"
         export PROJECT_DIR="$PROJECT_ROOT/$PROJECT/shots/$SHOT/$TASK" 
          }
Since filepath's are different for everyone doing this will ensure that every machine, every workstation and every artist is on the same page in the studio. 

 3. Load the pipeline in GITBash 
       source pipeline-demo/etc/pipeline-aliases.sh

 4. Make sure Maya is made visible to gitbash using the following commands: 
       alias mayapy="/c/Program Files/Autodesk/Maya2025/bin/mayapy.exe" 

## Usage
Using the Maya UI (inside Maya)

Open Maya

Load your script in the Script Editor

Run:

import assignment6


A window labeled "Make A Shape" will appear

Click Create My Ball

Choose red or purple to assign a shader

Repeat as many times as desired — the last ball created is the one affected by the shader buttons

## Contributing
This is an addition to the original assignment3.

## License
I am uploading this under the standard Github license. 
