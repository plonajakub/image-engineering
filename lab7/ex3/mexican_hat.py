import bpy
import math

mesh = bpy.data.meshes.new("Mexican Hat")
obj = bpy.data.objects.new(mesh.name, mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

N = 256
t_scale = 2.4
z_scale = 1
verts = []
for i in range(N):
    for j in range(N):
        x = (i - N / 2) / (N / 2)
        y = (j - N / 2) / (N / 2)
        t = ((x ** 2 + y ** 2) ** 0.5) * t_scale
        z = (1 - t ** 2) * math.exp(t ** 2 / -2) * z_scale
        verts.append((x, y, z))
        

def lin_idx(i, j):
    return N * i + j

faces = []
for i in range(N - 1):
    for j in range(N - 1):
        faces.append((lin_idx(i, j), lin_idx(i + 1, j),
                    lin_idx(i + 1, j + 1), lin_idx(i, j + 1)))

edges = []

mesh.from_pydata(verts, edges, faces)