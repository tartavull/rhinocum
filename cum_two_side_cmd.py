from __future__ import division
import os.path

import rhinoscriptsyntax as rs
import cum_read_gcode_cmd as  cumread
import cum_save_gcode_cmd as  cumsave

__commandname__ = "cum_two_side"

def get_hole():
    text = cumread.read_file('/Users/itq/rhinoscript/hole.nc')
    pts = list(cumread.get_coordinates(text))
    return rs.AddPolyline(pts)

def get_bottom_left(obj):
    box = rs.BoundingBox(obj)
    return box[0]

def get_top_right(obj):
    box = rs.BoundingBox(obj)
    return box[2]

def round_to_next_hole(x):
    return (x // 38.1 + 1) * 38.1

def hole_index(x):
    return int(round_to_next_hole(x) // 38.1)

def connect_polylines(polylines):
    points = []
    for polyline in polylines:
        points.extend(rs.PolylineVertices(polyline))
        rs.DeleteObject(polyline)
    return rs.AddPolyline(points)

def RunCommand(is_interactive, distance_to_piece=10):
    # Top part
    hole = cumread.get_polyline('/Users/itq/rhinoscript/hole.nc')
    piece_top = cumread.get_polyline()
    bl = get_bottom_left(piece_top)
    rs.MoveObject(piece_top, [-bl.X+distance_to_piece, 
                              -bl.Y+distance_to_piece,
                              0])

    new_hole = rs.CopyObject(hole)
    tr = get_top_right(piece_top)
    new_hole_x = round_to_next_hole(tr.X+distance_to_piece)
    new_hole_y = round_to_next_hole(tr.Y+distance_to_piece)
    rs.MoveObject(new_hole, [new_hole_x, new_hole_y, 0])

    connected = connect_polylines([hole,new_hole,piece_top])
    dirname = rs.BrowseForFolder("/Users/itq/Dropbox/cam/v2/")
    top_filename = 'shapeoko_top_holeX0_holeY0_holeX{}_holeY{}.nc'.format(hole_index(new_hole_x), hole_index(new_hole_y))
    bottom_filename = 'shapeoko_bottom_holeX0_holeY20_holeX{}_holeY{}.nc'.format(hole_index(new_hole_x), 20-hole_index(new_hole_y))
    cumsave.save(connected, 0, 0, os.path.join(dirname,top_filename))
    # Bottom part
    piece_bottom = cumread.get_polyline()
    rs.MoveObject(piece_bottom, [-bl.X+distance_to_piece, 
                                 bl.Y-distance_to_piece,
                                 0])
    cumsave.save(piece_bottom, 0, 20,  os.path.join(dirname, bottom_filename))

    """
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
    """
    print('file sucessfully saved')

if __name__ == "__main__":
    RunCommand(True)
