import bpy
import random
import math


def bpydeselect():
    bpy.ops.object.select_all(action='DESELECT')


def bpyselectall():
    bpy.ops.object.select_all(action='SELECT')


def bpyeditdeselect():
    bpy.ops.node.select_all(action='DESELECT')


def bpyeditselectall():
    bpy.ops.node.select_all(action='SELECT')


def bpydeleteall():
    bpyselectall()
    bpy.ops.object.delete(use_global=False)


def random_inside_unit_sphere(r = None):
    phi = random.uniform(0, 2 * math.pi)
    costheta = random.uniform(-1, 1)
    theta = math.acos(costheta)
    if r is None:
        u = random.uniform(0, 1) if r is None else r
        r = u**(1./3.)

    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)

    return [x, y, z]


def spherical_to_xyz(phi, theta, r):
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)

    return [x, y, z]
