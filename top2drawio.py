import sys

from xml.dom import minidom
from N2G import drawio_diagram

#Reading arg
input_file = sys.argv[1]

if not input_file:
    print('No input file, exiting')
    exit(1)

output_file = "Top.drawio"
if len(sys.argv) > 2:
    output_file = sys.argv[2]

#parsing input file
xmldoc = minidom.parse(input_file)

components = xmldoc.getElementsByTagName("import_component_type")
instances = xmldoc.getElementsByTagName("instance")
connections = xmldoc.getElementsByTagName("connection")

#creating diagram
diagram = drawio_diagram()
diagram.add_diagram("Top")

#reading all instances Top file
for instace in instances:
    node_id = instace.getAttribute("name")
    node_label = "{}: {}::{}".format(instace.getAttribute("name"), instace.getAttribute("namespace"), instace.getAttribute("type"))
    diagram.add_node(id=node_id, label=node_label)

#reading all connections
for con in connections:
    con_name = con.getAttribute("name")

    con_source = con.getElementsByTagName("source")[0]
    con_target = con.getElementsByTagName("target")[0]
    
    con_source_id = con_source.getAttribute("component")
    con_source_port = con_source.getAttribute("port")

    con_target_id = con_target.getAttribute("component")
    con_target_port = con_target.getAttribute("port")
    
    con_label = "{} -> {} -> {}".format(con_source_port, con_name , con_target_port)
    diagram.add_link(con_source_id, con_target_id, style='endArrow=classic;', label=con_label)

#preparing output
diagram.layout(algo="circle")
diagram.dump_file(filename=output_file, folder="./")