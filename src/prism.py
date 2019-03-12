#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
    QLineEdit, QApplication, QPushButton, QTextEdit)
from PyQt5.QtCore import pyqtSlot

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Return the stl program given the faces
# the faces are a list of three points
class StlEmbededWidget:
    def __init__(self, parent = None):
     QWidget.__init__(self, parent)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    @pyqtSlot()
    def on_click(self):
        self.button.setEnabled(False)
        try:
            name = (self.qle.text())
            length = int(self.qles.text())
            faces = int(self.qlesn.text())
            rotation = int(self.qlesnr.text())
            objec = button_action(name,length,faces,rotation)
            self.shower.setText(objec)
            show_stl(name)
        except:
            self.qle.setText("default")
            self.qles.setText("1")
            self.qlesn.setText("4")
            self.qlesnr.setText("0")
            objec = button_action()
            self.shower.setText(objec)
            show_stl()

        self.button.setEnabled(True)

    def initUI(self):

        self.lbl = QLabel(self)
        self.lbl.setText("Add the file name")
        self.qle = QLineEdit(self)

        self.lbl.move(60, 10)
        self.qle.move(60, 30)

        self.lble = QLabel(self)
        self.lble.setText("Add the edge size")
        self.qles = QLineEdit(self)

        self.lble.move(60, 50)
        self.qles.move(60, 70)

        self.lblen = QLabel(self)
        self.lblen.setText("Add the number of faces")
        self.qlesn = QLineEdit(self)

        self.lblen.move(60, 90)
        self.qlesn.move(60, 110)

        self.lblenr = QLabel(self)
        self.lblenr.setText("Add roation")
        self.qlesnr = QLineEdit(self)

        self.lblenr.move(60, 130)
        self.qlesnr.move(60, 150)

        self.button = QPushButton("Create STL", self)
        self.button.setToolTip("Create STL")
        self.button.move(60,210)
        self.button.clicked.connect(self.on_click)

        self.shower = QTextEdit(self)
        self.shower.move(220, 10)
        self.shower.setFixedWidth(240)
        self.shower.setFixedHeight(220)
        self.shower.setReadOnly(True)

        self.setFixedSize(500,250)
        self.setWindowTitle('STL-prism-creator')
        self.show()

def show_stl(name="default"):
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    your_mesh = mesh.Mesh.from_file("./"+name+".stl")
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors , facecolors='w', linewidths=1, alpha=0.5, edgecolors='#000000'))
    scale = your_mesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    pyplot.show()

def print_stl(faces):
    result = "solid cube \n"
    for face in faces:
        result = result + "facet normal 0 0 0 \n"
        result = result + "  outer loop \n"
        result = result + "    vertex " + str(face[0][0]) +" "+ str(face[0][1]) +" "+ str(face[0][2]) +" \n"
        result = result + "    vertex " + str(face[1][0]) +" "+ str(face[1][1]) +" "+ str(face[1][2]) +" \n"
        result = result + "    vertex " + str(face[2][0]) +" "+ str(face[2][1]) +" "+ str(face[2][2]) +" \n"
        result = result + "  endloop \n"
        result = result + "endfacet \n"
    result = result + "endsolid cube"
    return result

#Calculate the faces rotating and increasing
#height to the first 3 points calculated
def get_faces(longitud=1,lado=4,rotation=0):
    avg_lad = longitud/2
    b_angle = 360/lado
    avg = b_angle/2
    x = (avg_lad/math.tan(math.radians(avg)))
    z = avg_lad
    faces = []
    angle = rotation
    for i in range(0,lado):
        vertix_down = [[0,0,0]]

        figure_angle = math.radians(angle)

        xx = (x*math.cos(figure_angle)-z*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+z*math.cos(figure_angle))
        vertix_down.append([xx,zz,0])
        xx = (x*math.cos(figure_angle)-(-z)*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+(-z)*math.cos(figure_angle))
        vertix_down.append([xx,zz,0])
        faces.append(vertix_down)

        vertix_up = [[0,0,longitud]]
        xx = (x*math.cos(figure_angle)-z*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+z*math.cos(figure_angle))
        vertix_up.append([xx,zz,longitud])
        xx = (x*math.cos(figure_angle)-(-z)*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+(-z)*math.cos(figure_angle))
        vertix_up.append([xx,zz,longitud])
        faces.append(vertix_up)

        xx = (x*math.cos(figure_angle)-z*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+z*math.cos(figure_angle))
        vertix_left = [[xx,zz,longitud]]
        vertix_left.append([xx,zz,0])
        xx = (x*math.cos(figure_angle)-(-z)*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+(-z)*math.cos(figure_angle))
        vertix_left.append([xx,zz,0])
        faces.append(vertix_left)

        xx = (x*math.cos(figure_angle)-z*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+z*math.cos(figure_angle))
        vertix_right = [[xx,zz,longitud]]
        xx = (x*math.cos(figure_angle)-(-z)*math.sin(figure_angle))
        zz = (x*math.sin(figure_angle)+(-z)*math.cos(figure_angle))
        vertix_right.append([xx,zz,longitud])
        vertix_right.append([xx,zz,0])
        faces.append(vertix_right)
        angle = angle + b_angle

    return faces

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

def button_action(name="default",length=1,faces=4,rotation=0):
    faces = get_faces(length,faces,rotation)
    objec = print_stl(faces)
    file = open(name+".stl","w")
    file.write(objec)
    file.close()
    #print(objec)
    return objec

if __name__ == "__main__":
    main()