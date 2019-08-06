from __future__ import division
import rhinoscriptsyntax as rs

__commandname__ = "cum_save_gcode"

def program_start(write, x, y):
    for cmd in ("G21\n",
             "G90\n",
             "M6 T1\n",
             "M3 S5000\n",
             "G53 G0 X{} Y{}\n".format(*get_hole_location(x,y)),
             "G92 X0 Y0\n",
             "G1 G54 F2500.0\n"):
        write(cmd)

def get_hole_location(x, y):
    return -808.1+x*38.1, -765.1+y*38.1

def program_end(write):
    write('M5\n')
    write('M30\n')

def save(obj, x=0, y=0, filename=None):
    if filename is None:
        filename = rs.SaveFileName ("Save", "CarbideMotion (*.nc)|*.nc||")

    print('saving to ' + filename)
    with open(filename,'w') as f:
        program_start(f.write, x ,y)
        points = rs.PolylineVertices(obj)
        for point in points: 
            f.write("X{:.3f}Y{:.3f}Z{:.3f}\n".format(point.X, point.Y, point.Z))
        program_end(f.write)
    print('file sucessfully saved')

def RunCommand(is_interactive):
    obj = rs.GetObject("Select a polyline")
    if not rs.IsPolyline(obj):
        return
    save(obj)

if __name__ == "__main__":
    RunCommand(True)
