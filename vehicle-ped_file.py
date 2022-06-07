import xml.etree.ElementTree as ET
import time 

        
def read_net_file():
        
    path = "/home/mittal/VRU/All_one/ingolstadt.net.xml"
    tree = ET.parse(path)
    root = tree.getroot()

    edge_id = []
    edge_length = []
        
    for parent in root.findall('.//edge/..'):
        for element in parent.findall('edge'):
            edge_id.append(element.get('id')) 
            all_lanes= element.findall('lane')
            child=all_lanes[0]
            value = child.get('length')
            edge_length.append(float(value))


    #edge_length_new = ([i[0] for i in groupby(edge_length)])
                  
    print(len(edge_id),len(edge_length))
    zip_int = zip(edge_id,edge_length)
    dictonary = dict(zip_int)
    
    return dictonary


def find_length(ids,dictonary):
        y=ids.split()
        total_length = 0 
        for id in y:
        
            length = dictonary.get(id)
            
            if length != None :
                total_length+=length
            #print(id , '=' , length)
        return total_length

#Main entry
if __name__ == "__main__":

    start_time = time.time()

    #Read the net file to make memory of edge:length
    make_dictonary = read_net_file()

    path = "/home/mittal/VRU/All_one/persons.rou.xml"
    tree = ET.parse(path)
    root = tree.getroot()

    #create new-only-vehicle file to preserve the original file
    name = time.strftime("%Y\%m\%d--%I:%M:%S")
    path_copy = '/home/mittal/VRU/All_one/persons.'+name+'.rou.xml'
    tree.write(path_copy)

    #creating xml with only vehicles
    vehile_route_file = ET.parse(path_copy)
    root_vehile_route_file = vehile_route_file.getroot()
    #print(root_vehile_route_file.getChildren()[0])

    vehicle = 0
    edge_id_no = []
    pedestrians_id = []
    count = 0 

    for parent in root_vehile_route_file.findall('.//vehicle/.'):
        #print(type(parent))
        vehicle_id = (parent.get('id'))
        for child in parent.findall('route'):
                edge_ids = child.get('edges')
                each_route_length = find_length(edge_ids,make_dictonary)
                #print(vehicle_id ,':', each_route_length)
                if each_route_length < 350:
                    #print(parent.get('id'),each_route_length)
                    pedestrians_id.append(vehicle_id)
                    root_vehile_route_file.remove(parent)
                    count+= 1

                #edge_id_no.append(edge_ids)

                vehicle+=1

    vehile_route_file.write(path_copy,encoding='utf-8', xml_declaration=True)
    
    #creating xml with only pedestrains
    ped_path = '/home/mittal/VRU/All_one/persons.pedestrians.'+name+'.rou.xml'
    tree.write(ped_path)
    pedestrian_route_file = ET.parse(ped_path)
    root_pedestrian_route_file = pedestrian_route_file.getroot()


    i=0
    for parent in root_pedestrian_route_file.findall('.//vehicle/.'):
            if parent.get('id') not in pedestrians_id :
                root_pedestrian_route_file.remove(parent)
                i+=1
    pedestrian_route_file.write(ped_path,encoding='utf-8',xml_declaration=True)
    
    print('total users = ',vehicle,count,'vehicle=',i,'total ped=',vehicle-i)

    end_time= time.time()
    time_elasped = end_time - start_time
    print ('Execution time:',time_elasped)
