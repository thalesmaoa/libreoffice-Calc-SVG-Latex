# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
Thales Maia - 18/03/2016

The main problem regarding libreoffice svg export is that it creates many
subchilds. The first one loose the x,y position.

So we manually add it
"""

import xml.etree.ElementTree as ET
import subprocess, argparse

def main():
    # create parser
    parser = argparse.ArgumentParser(description="Reading SVG")
    # add expected arguments
    parser.add_argument('--file', dest='file', required=True)
    # parse args
    args = parser.parse_args()
    svg_file = args.file
    
    # Get svg
    tree = ET.parse(svg_file)
    root = tree.getroot()
    
    # Define spacing
    ET.register_namespace("","http://www.w3.org/2000/svg")
    # Look for xml tags with text
    for child in root.findall('{http://www.w3.org/2000/svg}text'):
        # Check if missing x coordinate
        if not 'x' in child[0].keys():
            # Get it from the first child / chid        
            if 'x' in child[0][0].keys():
                x_str = child[0][0].attrib['x']
                y_str = child[0][0].attrib['y']
                child.set("x", x_str)
                child.set("y", y_str)
            else:
                print "Coudn't find x,y coordinates"
                
    tree.write('aux.svg')
    subprocess.call(['/usr/bin/inkscape', '-D', '-z',  '--file=aux.svg', '--export-pdf=' + svg_file[:-3] + 'pdf', '--export-latex'])
    subprocess.call(['rm', 'aux.svg'])
    print 'File successfully created'

if __name__ == "__main__":
    main()
