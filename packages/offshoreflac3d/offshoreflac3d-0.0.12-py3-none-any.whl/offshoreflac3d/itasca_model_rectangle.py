import itasca as it
it.command("python-reset-state false")

#cur_dir = os.getcwd(sys.argv[0])
# cur_dir = os.path.dirname(os.path.abspath(__file__))
# it.command("[global cur_dir = system.directory()]")

# cur_dir = cur_dir= "G:\Software_Copyright\FALC3D_MPJFSCV2\multi_col_4"

# df_general = pd.read_excel(r"{}\SBJ_4_Input.xlsx".format(cur_dir), sheet_name = 'General')
# df_geometry = pd.read_excel(r"{}\SBJ_4_Input.xlsx".format(cur_dir), sheet_name = 'Geometry')
# df_soil = pd.read_excel(r"{}\SBJ_4_Input.xlsx".format(cur_dir), sheet_name = 'Soil')
# df_loads = pd.read_excel(r"{}\SBJ_4_Input.xlsx".format(cur_dir), sheet_name = 'Loads')
#


# #Meshing Parameters
# distance = df_geometry.values[3,2]
# scour_depth = df_geometry.values[3,4]
# boundary_x = df_geometry.values[4,2]
# boundary_y = df_geometry.values[4,4]
# boundary_z = df_geometry.values[4,6]
# radial_num_zone1 = df_geometry.values[5,2]
# radial_num_zone2 = df_geometry.values[6,2]
# radial_ratio1 = df_geometry.values[5,4]
# radial_ratio2 = df_geometry.values[6,4]

# #Geometry of Suction Buckets
# R = df_geometry.values[25,2] / 2.0
# L = df_geometry.values[25,4]
# t = df_geometry.values[25,6]


# #Soil Properties
# soil_layers = df_soil.values[4:,2]
# density = df_soil.values[4:,3]
# elastic = df_soil.values[4:,4]
# poisson = df_soil.values[4:,5]
# cohesion = df_soil.values[4:,6]
# friction = df_soil.values[4:,7]


def model_main(R,L,radial_num_zone1,radial_num_zone2,radial_ratio1,radial_ratio2,distance,boundary_x,boundary_y,scour_depth,soil_layers):
    layering = []
    for i in soil_layers:
        layering.append(i)
    layering.append(soil_layers[0]-scour_depth)
    layering.append(soil_layers[0]-L)
    layering.sort(reverse=True)
    # print(layering)
    #model new#########################
    it.command("model new")
    it.fish.set('R',R)
    it.fish.set('mudline',soil_layers[0])
    it.fish.set('scour_depth',scour_depth)
    it.fish.set('distance',distance)
    it.fish.set('boundary_x',boundary_x)
    it.fish.set('boundary_y',boundary_y)
    it.fish.set('boundary_z',soil_layers[-1])
    #basic model
    command1 = '''zone import 'zone_{}.inp' format abaqus
    zone group 'SC' slot 'suction caisson'
    '''.format(int(R))
    command2 = '''
    zone create radial-cylinder point 0 0  0  0 ...
                point 1 	[distance/2] 0 0 ...
                point 2 	0 0 1 ...
                point 3 	0 [-distance/2] 0 ...
                point 4 	[distance/2] 0 1 ...
                point 5 	0 [-distance/2] 1 ...
                point 6 	[distance/2] [-distance/2] 0 ...
                point 7 	[distance/2] [-distance/2] 1 ...
                point 8 	[R] 0 0 ...
                point 9 	0 [-R] 0 ...
                point 10 	[R] 0 1 ...
                point 11 	0 [-R] 1 ...
                size 6 1 12 {} ...
                ratio 1 1 1 {} ...
                group 'Block2' slot 'Block'
    ;zone reflect origin 0 0 0 normal 0 1 0 range group 'Block2' slot 'Block'
    '''.format(radial_num_zone1,radial_ratio1)
    command3 = '''
    zone group 'NoSC' slot 'suction caisson' range group 'SC' slot 'suction caisson' not
    zone reflect origin 0 0 0 normal 0 1 0 merge on
    zone reflect origin 0 0 0 normal 1 0 0 merge on
    '''
    it.command(command1)
    it.command(command2)
    it.command(command3)

    for gp in it.gridpoint.list():
        gp.set_pos_x(gp.pos_x()+distance/2)
        gp.set_pos_y(gp.pos_y()+distance/2)

    command = '''
    zone create radial-tunnel point 0 (0 0 0)...
                point 1 	[boundary_x] 	0 		0 ...
                point 2 	0 		0 		1 ...
                point 3 	0 		[-boundary_y] 	0 ...
                point 4 	[boundary_x] 	0 		1 ...
                point 5 	0 		[-boundary_y] 	1 ...
                point 6 	[boundary_x] 	[-boundary_y] 	0 ...
                point 7 	[boundary_x] 	[-boundary_y] 	1 ...
                point 8 	[distance] 	0 		0 ...
                point 9 	0 		[-distance] 	0 ...
                point 10 	[distance] 	0 		1 ...
                point 11 	0 		[-distance] 	1 ...
                point 12 	[distance] 	[-distance] 	0 ...
                point 13 	[distance] 	[-distance] 	1 ...
                size 12 1 12 {} ...
                ratio 1 1 1 {} ...
                group 'Block3' slot 'Block'
    zone reflect origin 0 0 0 normal 0 1 0 merge on
    zone reflect origin 0 0 0 normal 1 0 0 merge on
    '''.format(radial_num_zone2,radial_ratio2)
    it.command(command)
    #layering
    for gp in it.gridpoint.list():
        gp.set_pos_z(gp.pos_z()+soil_layers[0]-1)

    command_template = ("zone copy 0 0 {} merge on range position-z {} {}")

    for i in layering:
        if i == layering[0]:
            continue
        elif i == layering[-1]:
            continue
        else:
            it.command(command_template.format(i-layering[0],layering[0],layering[1]))
        
    for gp in it.gridpoint.list():    
        for i in range(len(layering)-1):
            if gp.pos_z() == layering[i]-1:
                gp.set_pos_z(layering[i+1])

    # print(soil_layers)
      
    for z in it.zone.list():
        for i in range(len(soil_layers)-1):
            if z.pos_z() <= soil_layers[i] and z.pos_z() >= soil_layers[i+1]:
                z.set_group("soil_{}".format(i),"soil")

    for i in range(len(layering)-1):
        if layering[i]-layering[i+1] <= 0.5:
            continue
        elif layering[i]-layering[i+1] > 0.5 and layering[i]-layering[i+1] < 1.0:
            it.command("zone densify global segments 1 1 2 range position-z {} {}".format(layering[i],layering[i+1]))
        else:
            if layering[0]-L < layering[i+1]:
                command = "zone densify global segments 1 1 {} range position-z {} {}"
                it.command(command.format(int(layering[i]-layering[i+1])*2,layering[i],layering[i+1]))
            else:
                command = "zone densify global segments 1 1 {} range position-z {} {}"
                it.command(command.format((int(layering[i]-layering[i+1])+1)*1,layering[i],layering[i+1]))

    it.command("zone attach by-face tolerance-absolute 0.1")
    it.command("model save 'model'")
    print("'Model' saved!")

# model_main(R,L,radial_num_zone1,radial_num_zone2,radial_ratio1,radial_ratio2,distance,boundary_x,boundary_y,scour_depth,soil_layers)
