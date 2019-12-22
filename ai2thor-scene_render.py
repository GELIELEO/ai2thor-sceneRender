#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Author: Eduardo Gutierrez Maestro
    Master Thesis 2018 - 2019
    Research Group : GRAM - University of Alcala
    Last Modification : 05.03.2019
'''
'''
:param  scene_name: Name of the scene to be rendered
:param  hdf5_name: Name of the output fil with the scene rendered
:param  gridSize: Size of the scene grid
:return: A HDF5 file with the information needed to navigate through the scene 

'''

import ai2thor.controller
import numpy as np
import h5py
import argparse


class ai2thor_scene_render():

    def __init__(self, scene_name, hdf5_name, gridSize):

        self.scene_name = scene_name
        self.hdf5_name = hdf5_name
        self.gridSize = gridSize

        self.controller = ai2thor.controller.BFSController()
        self.controller.start()

        self.controller.step(dict(action='Initialize', gridSize=self.gridSize))

        self.controller.search_all_closed(scene_name)  # replace with whatever scene you want
        self.points_scene = self.controller.grid_points


    def scene_render(self):
        N = len(self.points_scene)

        num_ID_total = N * 4
        self.rotations = np.zeros((num_ID_total,), dtype=np.uint64)
        self.locations = np.zeros((num_ID_total, 2), dtype=np.float64)

        self.rotations = self.assign_rotations()
        self.locations = self.assign_locations()
        self.transition_graph = self.assign_transition_graph(gridSize=self.gridSize)
        self.observations = np.zeros((num_ID_total, 300, 300, 3), dtype=np.uint8)

        aux = 0
        for i in range(len(self.points_scene)):
            _x = self.points_scene[i]['x']
            _y = self.points_scene[i]['y']
            _z = self.points_scene[i]['z']
            for rot in [0.0, 90.0, 180.0, 270.0]:
                event = self.controller.step(dict(action='TeleportFull', x=_x, y=_y, z=_z, rotation=rot))
                self.observations[aux, :, :, :] = event.frame
                aux += 1

        with h5py.File('data/' + self.hdf5_name, 'w') as hdf:
            hdf.create_dataset('rotation', data=self.rotations)
            hdf.create_dataset('location', data=self.locations)
            hdf.create_dataset('observation', data=self.observations)
            hdf.create_dataset('graph', data=self.transition_graph)

    def assign_rotations(self):
        done = False
        aux = 0
        while not done:
            for i in [0, 90, 180, 270]:
                self.rotations[aux] = i
                aux += 1
            if aux == len(self.rotations):
                done = True
        return self.rotations

    def assign_locations(self):

        x_z_tuple = np.zeros((np.size(self.points_scene, 0), 2))

        for i in range(len(self.points_scene)):
            _x = self.points_scene[i]['x']
            _z = self.points_scene[i]['z']

            x_z_tuple[i, 0] = _x
            x_z_tuple[i, 1] = _z

        aux = 0
        for i in range(len(x_z_tuple)):
            for _ in range(4):
                self.locations[aux] = x_z_tuple[i]
                aux += 1
        return self.locations

    #This function creates the transition graph needed to navigate in discrete way
    def assign_transition_graph(self, ACTION_SPACE=4, gridSize=0.25):

        id_tot_num = np.size(self.locations, 0)
        t_graph = np.zeros((id_tot_num, ACTION_SPACE), dtype=np.int64)
        for i in range(len(t_graph)):
            current_loc = self.locations[i]
            current_rot = self.rotations[i]
            for act in range(ACTION_SPACE):
                if act == 0:  # MoveAhead action in order to guess the ID
                    _x = current_loc[0]
                    _z = current_loc[1]

                    if current_rot == 0:
                        next_loc = [_x, _z + gridSize]
                    if current_rot == 90:
                        next_loc = [_x + gridSize, _z]
                    if current_rot == 180:
                        next_loc = [_x, _z - gridSize]
                    if current_rot == 270:
                        next_loc = [_x - gridSize, _z]

                    id_loc = np.where(np.all(self.locations == next_loc, axis=1))[0]

                    if np.size(id_loc) == 0:
                        t_graph[i, act] = -1  # We consider that if there is no location available
                        # is because there will be collision
                    else:
                        id_rot = np.where(self.rotations == current_rot)[0]
                        id_ahead = np.intersect1d(id_loc, id_rot)[0]
                        t_graph[i, act] = id_ahead

                if act == 1:  # RotateRight action in order to guess the ID
                    next_rot = current_rot + 90
                    if next_rot == 360:
                        next_rot = 0

                    id_loc = np.where(np.all(self.locations == current_loc, axis=1))[0]
                    id_rot = np.where(self.rotations == next_rot)[0]
                    id_right = np.intersect1d(id_loc, id_rot)[0]

                    t_graph[i, act] = id_right

                if act == 2:  # RotateLeft action in order to guess the ID
                    next_rot = current_rot - 90
                    if next_rot == -90:
                        next_rot = 270

                    id_loc = np.where(np.all(self.locations == current_loc, axis=1))[0]
                    id_rot = np.where(self.rotations == next_rot)[0]
                    id_left = np.intersect1d(id_loc, id_rot)[0]

                    t_graph[i, act] = id_left
                if act == 3:  # MoveBack action in order to guess the ID
                    _x = current_loc[0]
                    _z = current_loc[1]

                    if current_rot == 0:
                        next_loc = [_x, _z - gridSize]
                    if current_rot == 90:
                        next_loc = [_x - gridSize, _z]
                    if current_rot == 180:
                        next_loc = [_x, _z + gridSize]
                    if current_rot == 270:
                        next_loc = [_x + gridSize, _z]

                    id_loc = np.where(np.all(self.locations == next_loc, axis=1))[0]

                    if np.size(id_loc) == 0:
                        t_graph[i, act] = -1  # We consider that if there is no location available
                        # is because there will be collision
                    else:
                        id_rot = np.where(self.rotations == current_rot)[0]
                        id_back = np.intersect1d(id_loc, id_rot)[0]
                        t_graph[i, act] = id_back

        return t_graph

if __name__ == '__main__':

    scene1  = ai2thor_scene_render(
        scene_name='FloorPlan28',
        hdf5_name='scene_401.h5',
        gridSize=0.25
    )
    scene1.scene_render()

