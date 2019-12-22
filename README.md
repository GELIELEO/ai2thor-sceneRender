# AI2THOR Scene Render
This repository offers a solution to render a scene of the AI2THOR virtual navigation environment.
The main objective of this project is to offer an solution to the users that want to render scenes of the virtual environment AI2THOR.
The offered code gives a solution to discrete navigation. 

## How to use it
The python file ```ai2thor_scene_render.py``` consists on a class to create all the information needed to perform a discrete navigation within AI2THOR environment.
In sort, all we need to do in order to create the render of a new 
```python
scene1  = ai2thor_scene_render(
        scene_name='FloorPlan28',
        hdf5_name='scene_401.h5',
        gridSize=0.25
    )
```
