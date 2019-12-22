# AI2THOR Scene Render
This repository offers a solution to render a scene of the AI2THOR virtual navigation environment.
The main objective of this project is to offer an solution to the users that want to render scenes of the virtual environment AI2THOR.
The offered code gives a solution to discrete navigation. 

## How to use it
The python file ```ai2thor_scene_render.py``` consists on a class to create all the information needed to perform a discrete navigation within AI2THOR environment.
In sort, all we need to do in order to create the render of a new scene is to create an object of the class ```ai2thor_scene_render()```, as it is shown in the following piece of code:

```python
scene1  = ai2thor_scene_render(
        scene_name='FloorPlan28',
        hdf5_name='scene_401.h5',
        gridSize=0.25
    )
```
It is highlighted three parameters:

* scene_name : It is the name of the scene wished to be rendered.
* hdf5_name : Name of the output name.
* gridSize : This number corresponds to the size of the grid, i.e how much the agent will move within the scene.

Once one has created the object, it is as simple as calling the method ```scene_render()``` of the created object to render the new scene. The following code shows an example of how could be done:

```python
scene1.scene_render()
``
