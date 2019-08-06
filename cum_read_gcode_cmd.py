from __future__ import division
import re
import rhinoscriptsyntax as rs

__commandname__ = "cum_read_gcode"

def remove_return_carriage(line):
    return line[:-1]

def split_into_commands(line):
    commands = re.findall(r'(G\d+|M\d+|X\-?\d+\.\d*|Y\-?\d+\.\d*|Z\-?\d+\.\d*)+?', line)
    if not commands:
        raise RuntimeError(line + ' not understood')
    return iter(commands)

def read_file():
    #filename = rs.OpenFileName("Open", "STL(stereolithography) (*.stl)|*.stl||")
    filename = rs.OpenFileName("Open", "CarbideMotion (*.nc)|*.nc||")
    with open(filename, 'r') as f:
        for line in f:
            yield remove_return_carriage(line)

def get_commands(lines):
    for line in lines:
        if line.startswith('%'):
            # first program line
            pass
        elif line.startswith('('): 
            # comments
            pass
        else:
            for cmd in split_into_commands(line):
                yield cmd

def get_coordinates():
    x,y,z = None, None, None
    for cmd in get_commands(read_file()): 
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
            if x is None or y is None or z is None:
                continue
            yield x, y, z
        elif cmd.startswith('Y'):
            # coordinate
            y = float(cmd[1:])
            if x is None or y is None or z is None:
                continue
            yield x, y, z
        elif cmd.startswith('Z'):
            # coordinate
            z = float(cmd[1:])
            if x is None or y is None or z is None:
                continue
            yield x, y, z
        else:
            raise RuntimeError('unkown command '+ cmd)

def RunCommand(is_interactive):
    rs.AddPolyline(list(get_coordinates()))
    print('command ran')

if __name__ == "__main__":
    RunCommand(True)
