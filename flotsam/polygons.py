import math

# sum list of mass-centroid-pairs
def add_centroids(mbs):
    mt = sum([m for (m, _) in mbs])
    if abs(mt) < 10**(-5):
        return (0, (0, 0))
    xt = sum([m*x for (m, (x, _)) in mbs]) / mt
    yt = sum([m*y for (m, (_, y)) in mbs]) / mt
    return (mt, (xt, yt))

# area and centroid of triangle given by vertices
def triangle_centroid(a, b, c):
    p = ((a[0]+b[0]+c[0])/3, (a[1]+b[1]+c[1])/3)
    v = (b[0]-a[0], b[1]-a[1])
    w = (c[0]-a[0], c[1]-a[1])
    area = ( -v[1]*w[0] + v[0]*w[1] ) / 2
    return (area, p)

def polygon_centroid(verts):
    triangles = [ (verts[0], verts[i], verts[i+1])
                  for i in range(1, len(verts)-1)
                ]
    return add_centroids(
        [ triangle_centroid(a, b, c) for (a, b, c) in triangles ] )

def polygon_area(verts):
    if len(verts) <= 2:
        return 0
    (area, _) = polygon_centroid(verts)
    return area

def translated_polygon(v, verts):
    return [ (v[0]+vert[0], v[1]+vert[1]) for vert in verts ]

def centered_polygon(verts):
    (_, (v0, v1)) = polygon_centroid(verts)
    return translated_polygon((-v0, -v1), verts)

def rotated_polygon(alpha, verts):
    s = math.sin(alpha)
    c = math.cos(alpha)
    return [ (c*x - s*y, s*x + c*y) for (x, y) in verts ]

# intersect polygon with the half plane y <= 0
def cut_polygon(verts):
    newverts = []
    for i in range(len(verts)):
        a = verts[i-1]
        b = verts[i]
        if (a[1]<=0) != (b[1]<=0):
            t = -a[1] / (b[1]-a[1])
            newverts.append(((1-t)*a[0] + t*b[0], (1-t)*a[1] + t*b[1]))
        if b[1]<=0:
            newverts.append(b)
    return newverts
