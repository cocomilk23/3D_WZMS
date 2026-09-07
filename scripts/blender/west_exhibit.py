"""Map real reference exhibit panels onto planar meshes without inventing text."""
import bpy
from mathutils import Vector
import campus_common as c

def solve(a,b):
    a=[list(row)+[val] for row,val in zip(a,b)];count=len(a)
    for j in range(count):
        pivot=max(range(j,count),key=lambda i:abs(a[i][j]));a[j],a[pivot]=a[pivot],a[j]
        d=a[j][j];assert abs(d)>1e-10;a[j]=[q/d for q in a[j]]
        for i in range(count):
            if i!=j:
                q=a[i][j];a[i]=[u-q*v for u,v in zip(a[i],a[j])]
    return [row[-1] for row in a]

def photo_panel(name,centre,width,height,face,quad,horizontal=(1,0,0)):
    file=c.ROOT/f'reference/panoramas/faces/119232356/{face}.jpg'
    image=bpy.data.images.load(str(file),check_existing=True)
    if not image.packed_file:image.pack()
    mat=c.material('Alumni original exhibition photo '+face,(.5,.5,.5),.69)
    if len(mat.node_tree.nodes)==2:
        node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=image
        mat.node_tree.links.new(node.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    a,b=[],[]
    for (x,y),(u,v) in zip([(0,0),(1,0),(1,1),(0,1)],quad):
        u/=1600;v/=1600
        a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);b.extend([u,v])
    hh=solve(a,b)+[1];verts,faces,uv=[],[],[];count=20;origin=Vector(centre);axis=Vector(horizontal)
    for j in range(count+1):
        for i in range(count+1):
            x=i/count;y=1-j/count;den=hh[6]*x+hh[7]*y+1
            verts.append(origin+axis*((x-.5)*width)+Vector((0,0,j/count*height)))
            uv.append(((hh[0]*x+hh[1]*y+hh[2])/den,1-(hh[3]*x+hh[4]*y+hh[5])/den))
    for j in range(count):
        for i in range(count):k=j*(count+1)+i;faces.append((k,k+1,k+count+2,k+count+1))
    obj=c.mesh(name,verts,faces,mat);layer=obj.data.uv_layers.new(name='Original photo projective mapping')
    for face in obj.data.polygons:
        for loop in face.loop_indices:layer.data[loop].uv=uv[obj.data.loops[loop].vertex_index]
    obj['reference_file']=file.relative_to(c.ROOT).as_posix();obj['source_quad_on_1600px_face']=str(quad)
    return obj
