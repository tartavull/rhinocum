from __future__ import division
import re
import rhinoscriptsyntax as rs

__commandname__ = "cum_read_gcode"

def remove_return_carriage(line):
    return line[:-1]

def split_into_commands(line):
    commands = re.findall(r'(G\d+|M\d+|X\-?\d+\.\d*|Y\-?\d+\.\d*|Z\-?\d+\.\d*|A\-?\d+\.\d*|F\d+\.\d*|S\d+|T\d+\s?)+?', line)
    if len(''.join(commands)) != len(line):
        print(''.join(commands), line)
    if not commands:
        raise RuntimeError(line + ' not understood')
    return commands

def read_file(filename=None):
    #filename = rs.OpenFileName("Open", "STL(stereolithography) (*.stl)|*.stl||")
    #filename = '/Users/itq/Desktop/top.nc'
    if filename is None:
        filename = rs.OpenFileName("Open", "CarbideMotion (*.nc)|*.nc||")
    with open(filename, 'r') as f:
        for line in f:
            yield remove_return_carriage(line)

def get_statements(lines):
    for line in lines:
        if line.startswith('%'):
            # first program line
            pass
        elif line.startswith('('): 
            # comments
            pass
        else:
            yield split_into_commands(line)

def get_coordinates(lines):
    x,y,z = None, None, None
    pos_updated = False
    for statement in get_statements(lines):
        for cmd in statement: 
            if cmd == 'G0':
                # rapid linear movement, no material cutting
                pass
            elif cmd == 'G1':
                # rapid linear movement, cutting material
                pass
            elif cmd == 'G21':
                # Set units to millimeters
                pass
            elif cmd == 'G90':
                # Absolute Positioning
                pass
            elif cmd == 'M3':
                # Spindle CW
                pass
            elif cmd == 'M5':
                # Spindle Stop
                pass
            elif cmd == 'M6':
                # Tool Change
                pass
            elif cmd == 'M30':
                # Program End
                pass
            elif cmd.startswith('X'):
                # coordinate
                x = float(cmd[1:])
                pos_updated = True
            elif cmd.startswith('Y'):
                # coordinate
                y = float(cmd[1:])
                pos_updated = True
            elif cmd.startswith('Z'):
                # coordinate
                z = float(cmd[1:])
                pos_updated = True
            elif cmd.startswith('A'):
                # coordinate
                # A-axis is ignored
                pass
            elif cmd.startswith('F'):
                #Feedrate
                pass
            elif cmd.startswith('S'):
                #Spindle Speed
                pass
            elif cmd.startswith('T'):
                #Set tool number
                pass
            else:
                raise RuntimeError('unkown command '+ cmd)
        if pos_updated:
            if x is None or y is None or z is None:
                continue
            yield x, y, z
            pos_updated = False

def get_polyline(filename=None):
    #return list(get_coordinates(read_file(filename)))
    return rs.AddPolyline(list(get_coordinates(read_file(filename))))

def RunCommand(is_interactive):
    get_polyline()

if __name__ == "__main__":
    RunCommand(True)
