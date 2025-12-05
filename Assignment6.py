"""
Sphere pipeline tool (pipeline-safe, mayapy)

- Reads PROJECT, SHOT, TASK, ASSET, PROJECT_DIR / MAYA_PROJECT from environment.
- Uses argparse for CLI flags:
    --create   → create a sphere
    --color    → red or purple
    --save     → save a .mb file into an exports folder under PROJECT_DIR

Notes / references:
- os.getenv: https://docs.python.org/3/library/os.html#os.getenv
- argparse.ArgumentParser / add_argument: https://docs.python.org/3/library/argparse.html
- maya.cmds.file: see Autodesk Maya cmds.file docs
- General Maya Python workflow: Chad Vernon, "Python Scripting for Maya Artists"
"""

#Imports###########
import os.getenv("MAYA_PROJECT")
import argparse
import maya.standalone
import sys
import datetime
from datetime import datetime
import maya.cmds as cmds
import json

maya.standalone.initialize()
#Argument Parsing##
parser = argparse.ArgumentParser()
parser.add_argument("--create", action="store_true", help="Create the sphere.")
parser.add_argument("--color", type=str, help="set the sphere color", choices=['red', 'purple'])
parser.add_argument("--save", action="store_true", help="save the result")
args = parser.parse_args()

#Global Variables## 
PROJECT= os.getenv("PROJECT","defaultProject")
 #look for an environment variable called PROJECT, if not found or does not exist use the literal string of defaultProject
SHOT = os.getenv("SHOT","0000")
SCENE = os.getenv("SCENE","defaultScene")
    #look for an environment variable called SHOT, if not found use 0000
WIN = "SphereColorWin"
STATE = {"sphere": None}
ASSET = os.getenv("ASSET","mySphereAsset")
PROJECT_DIR = os.getenv("PROJECT_DIR") or os.getenv("MAYA_PROJECT")

if not PROJECT_DIR: 
    sys.stderr.write(
        "[ERROR]PROJ_DIR or MAYA PROJECT is not currently in your environment .\n"
        "Make sure you run something like: \n"
        "project myproject\n"
        "shot myshot0010 model\n"
        "in Git Bash before running mayapy.\n"
    )
    maya.standalone.uninitialize()
    sys.exit(1)

# Build an exports directory under the pipeline project dir.
EXPORT_DIR = os.path.join(PROJECT_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# Filename: <asset>_sphere.mb (e.g. trex_sphere.mb)
filename = f"{ASSET}_sphere.mb"
OUTPUT_PATH = os.path.join(EXPORT_DIR, filename)
    
#Functions##
 
 def ensure_shader(name, rgb):
    """
    Create or reuse a lambert shader with the given RGB,
    and return its shading group.

    Uses maya.cmds.shadingNode, setAttr, sets, connectAttr.
    """
    if not cmds.objExists(name):
        shader = cmds.shadingNode("lambert", asShader=True, name=name)
    else:
        shader = name

    r, g, b = rgb
    cmds.setAttr(f"{shader}.outColor", r, g, b, type="double3")

    sg = name + "SG"
    if not cmds.objExists(sg):
        sg = cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=sg
        )

    if not cmds.listConnections(f"{shader}.outColor", s=False, d=True, p=True) or \
       not cmds.listConnections(f"{sg}.surfaceShader", s=True, d=False, p=True):
        try:
            cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", f=True)
        except Exception:
            # Avoid hard-crashing if connection already exists or fails
            pass

    return sg


def create_sphere(*_):
    """
    Create a poly sphere and remember it in STATE["sphere"].
    """
    xform, _ = cmds.polySphere(name="mySphere", radius=1.0)
    STATE["sphere"] = xform
    cmds.select(xform)
    print("[INFO] Created sphere:", xform)


def assign_color(rgb, base_name):
    """
    Assign a lambert of the given color to the current sphere.
    """
    xform = STATE.get("sphere")
    if not xform or not cmds.objExists(xform):
        cmds.warning("Make the ball before you change its color!")
        return

    sg = ensure_shader(base_name, rgb)
    cmds.sets(xform, e=True, forceElement=sg)
    print(f"[INFO] Assigned {base_name} to {xform}")


def color_red(*_):
    assign_color((1.0, 0.0, 0.0), "Z_RedLambert")


def color_purple(*_):
    assign_color((0.5, 0.0, 0.5), "Z_PurpleLambert")


# ------------------------------------------------------------
# 4. Apply CLI actions in order: create → color → save
# ------------------------------------------------------------

try:
    if args.create:
        create_sphere()

    if args.color == "red":
        color_red()
    elif args.color == "purple":
        color_purple()

    if args.save:
        # Use the pipeline-aware OUTPUT_PATH we built from PROJECT_DIR.
        cmds.file(rename=OUTPUT_PATH)
        # maya.cmds.file reference: Autodesk docs (type is optional but clearer).
        cmds.file(save=True, type="mayaBinary")
        print(f"[OK] Saved sphere to: {OUTPUT_PATH}")

#------------------------------------------------------------
# 5. Create python dictionary of stored data ###################
#------------------------------------------------------------

scene_metadata = {}
scene_metadata["project"] = PROJECT
scene_metadata["shot"] = SHOT
scene_metadata["scene"] = SCENE
scene_metadata["asset"] = ASSET
scene_metadata["output_path"] = OUTPUT_PATH
scene_metadata["updated_artist"]= os.getenv("USERNAME") or "unknown"
scene_metadata["updated_time"]= str(datetime.now())
print("[INFO] Scene metadata:", scene_metadata)
with open("scene_metadata.json", "w") as f:
    json.dump(scene_metadata, f, indent=4)
print(f"[OK] Wrote scene metadata to {scene_metadata.json}")
    finally:
    # Cleanly uninitialize Maya standalone when done.
    maya.standalone.uninitialize()