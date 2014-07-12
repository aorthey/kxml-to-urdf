from BeautifulSoup import BeautifulSoup
import os
import re
import sys

if len(sys.argv) != 2:
  print "usage: parser <kxml filename> "
  sys.exit(1)

kxml_fname = sys.argv[1]
urdf_fname = os.path.splitext(kxml_fname)[0]+'.urdf'

print "Converting "+kxml_fname+" to "+urdf_fname

## header for URDF
soup = BeautifulSoup(open(kxml_fname))
fh = open('env.urdf','w')
fh.write('<?xml version="1.0"?>\n')
fh.write('<robot name="wall_description">\n')

boxes = soup.scene.geometry_node.assembly.findAll("box")

for i in range(0,len(boxes)):
  sx = 0
  sy = 0
  sz = 0
  box = boxes[i]
  bid = int(box["id"])

  sx = float(box.find("property", {"stringid": "BOX_X_SIZE"}).text)
  sy = float(box.find("property", {"stringid": "BOX_Y_SIZE"}).text)
  sz = float(box.find("property", {"stringid": "BOX_Z_SIZE"}).text)

  pos = box.relative_position.text
  pos = re.split(' |\n',pos)
  x = float(pos[3])
  y = float(pos[7])
  z = float(pos[11])

  color = box.find("property", {"stringid": "GEOMETRY_DIFFUSE_COLOR"}).text
  color = re.split(' |\n',color)
  r = float(color[0])
  g = float(color[1])
  b = float(color[2])
  a = float(color[3])

  strL = '<link name="box%d">\n' % (bid)
  strL += '  <visual>\n'
  strL += '    <geometry>\n'
  strL += '      <box size="%f %f %f"/>\n' % (sx,sy,sz)
  strL += '    </geometry>\n'
  strL += '  <origin rpy="0 0 0" xyz="%f %f %f"/>\n' % (x,y,z)
  strL += '  <material name="wall_colored">\n'
  strL += '    <color rgba="%f %f %f %f"/>\n' % (r,g,b,a)
  strL += '  </material>\n'
  strL += '  </visual>\n'
  strL += '  <collision>\n'
  strL += '    <geometry>\n'
  strL += '      <box size="%f %f %f"/>\n' % (sx,sy,sz)
  strL += '    </geometry>\n'
  strL += '  </collision>\n'
  strL += '</link>\n'
  fh.write(strL)

#FOOTER
fh.write('</robot>\n')
print "Output written to "+urdf_fname
fh.close()
