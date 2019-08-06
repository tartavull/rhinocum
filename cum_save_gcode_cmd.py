from __future__ import division
import rhinoscriptsyntax as rs

__commandname__ = "cum_save_gcode"

def program_start(write):
    for cmd in ("G21\n",
             "G90\n",
             "M6 T1\n",
             "M3 S5000\n",
             "G1 F2500.0\n"):
        write(cmd)

def program_end(write):
    write('M5\n')
    write('M30\n')

def RunCommand(is_interactive):
    obj = rs.GetObject("Select a polyline")
    if not rs.IsPolyline(obj):
        return

    filename = rs.SaveFileName ("Save", "CarbideMotion (*.nc)|*.nc||")
    with open(filename,'w') as f:
        program_start(f.write)
        points = rs.PolylineVertices(obj)
        for point in points: 
            f.write("X{:.3f}Y{:.3f}Z{:.3f}\n".format(point.X, point.Y, point.Z))
        program_end(f.write)
    print('file sucessfully saved')

if __name__ == "__main__":
    RunCommand(True)
