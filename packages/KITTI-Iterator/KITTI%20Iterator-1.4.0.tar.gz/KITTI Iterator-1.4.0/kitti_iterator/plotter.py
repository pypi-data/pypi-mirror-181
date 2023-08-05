from ctypes.wintypes import POINT
import numpy as np
import os

###
# Plotter Code
###
#
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys

from pyqtgraph import Vector

import math
import matplotlib as mpl
cmap = mpl.colormaps['viridis']
# cmap = mpl.colormaps['magma']


global POINTS
global point_cloud_array
POINTS = []
MESHES = {
    'vertexes': [],
    'faces': [], 
    # 'vertexColors': [], 
    'faceColors': []
}
def dist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)**0.5

global min_height, max_height, colors, calculated, max_dist, min_dist, dist_range
calculated = False
colors_enabled = True

colors_hash = []
colors_hash_res = 10
for i in range(0,colors_hash_res):
    colors_hash.append(cmap(float(i)/(colors_hash_res-1)))

def update_graph():
    global graph_region, POINTS, MESHES, point_cloud_array, mesh_region
    global min_height, max_height, colors, calculated, max_dist, min_dist, dist_range
    global app
    
    try:
        if not point_cloud_array.empty():
            DATA = point_cloud_array.get()
            POINTS = DATA['POINTS']
            MESHES = DATA['MESHES']
        
        def col_map(index):
            return colors_hash[round(index*(colors_hash_res-1))]

        #POINTS = [(0,0,1), ]
        COLORS = np.ones(shape=(len(POINTS), 3), dtype=np.uint8)
        if len(POINTS)>0:
            POINTS = np.array(POINTS)
            
            if colors_enabled:
                heights = POINTS[:,2]
                
                max_height = np.max(heights)
                min_height = np.min(heights)
                # print('min_height, max_height', min_height, max_height)

                # max_height = 1.1
                # min_height = -3.5

                heights = (heights - min_height)/(max_height-min_height)
                heights_color_index = np.rint(heights*(colors_hash_res-1)).astype(np.uint8)
                
                COLORS = np.array([colors_hash[xi] for xi in heights_color_index])
            
            #POINTS_scaled = POINTS / 10000.0
            POINTS_scaled = POINTS.copy()
            # POINTS_scaled[:,2] = POINTS_scaled[:,2]*10.0
            # POINTS_scaled[:,2] += 10.0
            #print(POINTS)
            graph_region.setData(pos=POINTS_scaled, color=COLORS)
            #graph_region.setData(pos=POINTS)

        if 'vertexes' in MESHES and len(MESHES['vertexes'])>0:
            mesh_region.setMeshData(
                vertexes=MESHES['vertexes'], 
                faces=MESHES['faces'], 
                #vertexColors=MESHES['vertexColors'], 
                faceColors=MESHES['faceColors']
            )
    except KeyboardInterrupt:
        app.closeAllWindows()


def start_graph(points_q):
    global POINTS, point_cloud_array
    point_cloud_array = points_q
    
    print("Setting up graph")
    global app, graph_region, mesh_region, w, g, d3, t
    # app = QtGui.QApplication([])
    app = QtWidgets.QApplication([])
    w = gl.GLViewWidget()
    w.resize(800, 600)
    w.opts['distance'] = 20
    w.show()
    w.setWindowTitle('LIDAR Point Cloud')

    w.cameraPosition()
    w.setCameraPosition(pos=QtGui.QVector3D(0, 0, 0), )

    g = gl.GLGridItem()
    w.addItem(g)

    graph_region = gl.GLScatterPlotItem(pos=np.zeros((1, 3), dtype=np.float32), color=(0, 1, 0, 0.5), size=0.3, pxMode=False)
    # graph_region.translate(0, 0, 1.7)
    # graph_region.rotate(-90, 1, 0, 0)

    vertexes = np.array([[1, 0, 0], #0
                     [0, 0, 0], #1
                     [0, 1, 0], #2
                     [0, 0, 1], #3
                     [1, 1, 0], #4
                     [1, 1, 1], #5
                     [0, 1, 1], #6
                     [1, 0, 1]])#7

    faces = np.array([[1,0,7], [1,3,7],
                  [1,2,4], [1,0,4],
                  [1,2,6], [1,3,6],
                  [0,4,5], [0,7,5],
                  [2,4,5], [2,6,5],
                  [3,6,5], [3,7,5]])

    colors = np.array([[1,0,0,1] for i in range(12)])

    mesh_region = gl.GLMeshItem(
        vertexes=vertexes, faces=faces, faceColors=colors, drawEdges=True, edgeColor=(0, 0, 0, 1),
    )
    # mesh_region.translate(0, 0, 1.7)
    # mesh_region.rotate(180, 1, 0, 0)

    w.addItem(mesh_region)
    #graph_region.rotate(90 + 135, 1, 0, 0)
    w.addItem(graph_region)
    t = QtCore.QTimer()
    t.timeout.connect(update_graph)
    t.start(500)

    QtGui.QApplication.instance().exec_()
    print("\n[STOP]\tGraph Window closed. Stopping...")


def lidar_measurement_to_np_array(lidar_measurement):
    data = list()
    for location in lidar_measurement:
        data.append([location.x, location.y, location.z])
    return np.array(data).reshape((-1, 3))

def plot_points(data):
    #try:
    global POINTS
    POINTS = np.array(data)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        from multiprocessing import Queue
        point_cloud_array = Queue()
        start_graph(point_cloud_array)
