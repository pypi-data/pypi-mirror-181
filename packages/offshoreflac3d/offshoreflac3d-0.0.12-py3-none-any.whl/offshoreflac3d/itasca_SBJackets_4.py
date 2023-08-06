import numpy as np 
from shapely import geometry as geo
import itasca as it
it.command("python-reset-state false")


# #coordinates input###################
# v1 = [[8.0,8.0,24.0]]
# v2 = [[17.5,17.5,-30.5]]
# H_list = [24.0,8.0,-10.5,-32.5,-58.7]
# mudline = -34
# #GuoDuDuan input####################
# h_high = 31
# x_radial = 7.5/2
# #size of suction caisson############
# R = 20.0/2
# L = 22

def Jacket_main(v1,v2,H_list,mudline,h_high,x_radial,R,L,scour_depth):
    #print(v1)
    #Derived Inputs#####################
    h_low = v1[0][2]
    x_1 = v1[0][0]
    x_2 = v1[0][0]+1.0
    y_1 = x_1
    y_2 = x_2

    #K-nodes coordinates########################
    theta_radian = ((v2[0][0]-v1[0][0])*np.sqrt(2))/(v1[0][2]-v2[0][2])

    Delta_h = []
    for i in range(len(H_list)):
        temp = H_list[0] - H_list[i]
        Delta_h.append(temp)

    #print(Delta_h)
    # print(v1[0])
    #print(v1)
    def K_coordinats(v1,h):
        v_target = [0,0,0]
        v_target[0] = v1[0][0] +  h*theta_radian*np.sqrt(2)/2
        v_target[1] = v_target[0]
        v_target[2] = v1[0][2] - h
        return v_target
    
    for i in range(len(Delta_h)):
        if i == 0:
            pass
        else:
            #del v1[1]
            v1.append(K_coordinats(v1,Delta_h[i]))

    #print(v1)
    
    print('-----------------------------------------')

    for i in range(len(v1)):
        v1[i]=tuple(v1[i])

    #print(np.array(v1[0])*(1,-1,1))

    #X-nodes coordinates########################
    ##example
    #line1 = geo.LineString([np.array(v1[1]),np.array(v1[2])*(1,-1,1)])
    #line2 = geo.LineString([np.array(v1[2]),np.array(v1[1])*(1,-1,1)])
    #
    #print(line1.intersection(line2))

    def X_coordinates():
        v_X = []
        for i in range(len(v1)-1):
            line1 = geo.LineString([np.array(v1[i]),np.array(v1[i+1])*(1,-1,1)])
            line2 = geo.LineString([np.array(v1[i+1]),np.array(v1[i])*(1,-1,1)])
            point = geo.Point(line1.intersection(line2))
            v_X.append(point.coords[:])
            #print(line1.intersection(line2))
        return v_X

    v_X = X_coordinates()
    #print(v_X)
    print(v1)
    #itasca.file########################
    #it.fish.set('dr0', dr0)
    it.command("model restore 'Initial'")
    for i in range(len(v1)-1):
        print(i)
        #print(tuple(np.array(v1[i])*(-1,1,1)))
        command1 = "struct beam creat by-line {} {} id 11 group 'zhutui' slot 'jacket' segments {}".format(tuple(np.array(v1[i])*(1,1,1)),tuple(np.array(v1[i+1])*(1,1,1)),int(Delta_h[i+1]/8))
        command2 = "struct beam creat by-line {} {} id 11 group 'zhutui' slot 'jacket' segments {}".format(tuple(np.array(v1[i])*(-1,1,1)),tuple(np.array(v1[i+1])*(-1,1,1)),int(Delta_h[i+1]/8))
        command3 = "struct beam creat by-line {} {} id 11 group 'zhutui' slot 'jacket' segments {}".format(tuple(np.array(v1[i])*(1,-1,1)),tuple(np.array(v1[i+1])*(1,-1,1)),int(Delta_h[i+1]/8))
        command4 = "struct beam creat by-line {} {} id 11 group 'zhutui' slot 'jacket' segments {}".format(tuple(np.array(v1[i])*(-1,-1,1)),tuple(np.array(v1[i+1])*(-1,-1,1)),int(Delta_h[i+1]/8))
        it.command(command1)
        it.command(command2)
        it.command(command3)
        it.command(command4)
        #print(command)

    for i in range(len(v_X)):
        #print(v_X[i][0])
        command1 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X[i][0],tuple(np.array(v1[i])*(1,1,1)))
        command2 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X[i][0],tuple(np.array(v1[i+1])*(1,1,1)))
        command3 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X[i][0],tuple(np.array(v1[i])*(1,-1,1)))
        command4 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X[i][0],tuple(np.array(v1[i+1])*(1,-1,1)))
        it.command(command1)
        it.command(command2)
        it.command(command3)
        it.command(command4)
        #print(tuple(np.array(v_X[i][0])*(-1,-1,1)))
        v_X_temp = tuple(np.array(v_X[i][0])*(-1,-1,1))
        command5 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i])*(-1,1,1)))
        command6 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i+1])*(-1,1,1)))
        command7 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i])*(-1,-1,1)))
        command8 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i+1])*(-1,-1,1)))
        it.command(command5)
        it.command(command6)
        it.command(command7)
        it.command(command8)
        v_X_temp = tuple(np.array(v_X[i][0])*(0,v_X[i][0][1],1)+(0,v_X[i][0][0],0))
        command9 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i])*(-1,1,1)))
        command10= "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i+1])*(-1,1,1)))
        command11= "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i])*(1,1,1)))
        command12= "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i+1])*(1,1,1)))
        it.command(command9 )
        it.command(command10)
        it.command(command11)
        it.command(command12)
        v_X_temp = tuple(np.array(v_X[i][0])*(0,v_X[i][0][1],1)+(0,-v_X[i][0][0],0))
        command9 = "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i])*(1,-1,1)))
        command10= "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i+1])*(1,-1,1)))
        command11= "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i])*(-1,-1,1)))
        command12= "struct beam creat by-line {} {} id 11 group 'xietui' slot 'jacket' segments 6".format(v_X_temp,tuple(np.array(v1[i+1])*(-1,-1,1)))
        it.command(command9 )
        it.command(command10)
        it.command(command11)
        it.command(command12)

    print("jacket built!")
    #LianJieDuan############################################
    #print(tuple(np.array(v2[0])*(1,1,0)+(0,0,mudline)))

    delta = 1

    command1 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(1,1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(1,1,0)+(0,0,mudline)))
    command2 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(-1,1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(-1,1,0)+(0,0,mudline)))
    command3 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(1,-1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(1,-1,0)+(0,0,mudline)))
    command4 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(-1,-1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(-1,-1,0)+(0,0,mudline)))
    it.command(command1)
    it.command(command2)
    it.command(command3)
    it.command(command4)
    #
    command1 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 2".format(tuple(np.array(v2[0])*(1,1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(1,1,1)))
    command2 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 2".format(tuple(np.array(v2[0])*(-1,1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(-1,1,1)))
    command3 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 2".format(tuple(np.array(v2[0])*(1,-1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(1,-1,1)))
    command4 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 2".format(tuple(np.array(v2[0])*(-1,-1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(-1,-1,1)))
    it.command(command1)
    it.command(command2)
    it.command(command3)
    it.command(command4)
    #
    for theta in range(0,360,45):
        command1 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(1,1,0)+(0,0,mudline)),tuple(np.array(v2[0])*(1,1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        command2 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(-1,1,0)+(0,0,mudline)),tuple(np.array(v2[0])*(-1,1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        command3 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(1,-1,0)+(0,0,mudline)),tuple(np.array(v2[0])*(1,-1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        command4 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(-1,-1,0)+(0,0,mudline)),tuple(np.array(v2[0])*(-1,-1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        it.command(command1)
        it.command(command2)
        it.command(command3)
        it.command(command4)
        command5 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(1,1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(1,1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        command6 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(-1,1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(-1,1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        command7 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(1,-1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(1,-1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        command8 = "structure beam create by-line {} {} id 11 group 'lianjieduan' slot 'jacket' segments 3".format(tuple(np.array(v2[0])*(-1,-1,1)+(0,0,-delta)),tuple(np.array(v2[0])*(-1,-1,0)+(R*np.sin(theta/180*np.pi),R*np.cos(theta/180*np.pi),mudline)))
        it.command(command5)
        it.command(command6)
        it.command(command7)
        it.command(command8)

    it.command("structure link delete range group 'lianjieduan' slot 'jacket'")

    print("LianJieDuan built!")
    #GuoDuDuan############################################
    command1 = "structure beam create by-line {} {} id 11 group 'zhutui' slot 'GuoDuDuan' segments 2".format(tuple(np.array(v1[0])*(1,1,1)),tuple(np.array(v1[0])*(1,1,0)+(0,0,H_list[0]+1)))
    command2 = "structure beam create by-line {} {} id 11 group 'zhutui' slot 'GuoDuDuan' segments 2".format(tuple(np.array(v1[0])*(-1,1,1)),tuple(np.array(v1[0])*(-1,1,0)+(0,0,H_list[0]+1)))
    command3 = "structure beam create by-line {} {} id 11 group 'zhutui' slot 'GuoDuDuan' segments 2".format(tuple(np.array(v1[0])*(1,-1,1)),tuple(np.array(v1[0])*(1,-1,0)+(0,0,H_list[0]+1)))
    command4 = "structure beam create by-line {} {} id 11 group 'zhutui' slot 'GuoDuDuan' segments 2".format(tuple(np.array(v1[0])*(-1,-1,1)),tuple(np.array(v1[0])*(-1,-1,0)+(0,0,H_list[0]+1)))
    it.command(command1)
    it.command(command2)
    it.command(command3)
    it.command(command4)
    #
    it.fish.set('h_high',h_high)
    it.fish.set('h_low',h_low)
    it.fish.set('x_radial',x_radial)
    it.fish.set('x_1',x_1)
    it.fish.set('x_2',x_2)
    it.fish.set('y_1',y_1)
    it.fish.set('y_2',y_2)

    it.command('''
    zone create cylinder point 0 0 0 [h_low] ...
                point 1 [x_radial] 	0 				[h_low] ...
                point 2 0 			0 				[h_high] ...
                point 3 0 			[-x_radial] 	[h_low] ...
                point 4 [x_radial] 	0 				[h_high] ...
                point 5 0 			[-x_radial] 	[h_high] ...
                size [int(x_radial)*2] [int(h_high-h_low)] ...
                group 'Block1' slot 'Block'

    zone create radial-cylinder point 0 0  0  [h_low] ...
                point 1 	[x_1]  		0  			[h_low] ...
                point 2 	0  			0  			[h_high] ...
                point 3 	0 			[-y_1]  	[h_low] ...
                point 4 	[x_1]  		0  			[h_high] ...
                point 5 	0 			[-y_1]  	[h_high] ...
                point 6 	[x_1] 		[-y_1]  	[h_low] ...
                point 7 	[x_1] 		[-y_1]  	[h_high] ...
                point 8 	[x_radial] 	0 			[h_low] ...
                point 9 	0 			[-x_radial] [h_low] ...
                point 10 	[x_radial] 	0 			[h_high] ...
                point 11 	0 			[-x_radial] [h_high] ...
                size [int(x_radial)*2] [int(h_high-h_low)] ...
                group 'Block2' slot 'Block'
                
    zone create radial-tunnel point 0 (0 0 [h_low])...
                point 1 	[x_2] 	0 		[h_low] ...
                point 2 	0 		0 		[h_high] ...
                point 3 	0 		[-y_2] 	[h_low] ...
                point 4 	[x_2] 	0 		[h_high] ...
                point 5 	0 		[-y_2] 	[h_high] ...
                point 6 	[x_2] 	[-y_2] 	[h_low] ...
                point 7 	[x_2] 	[-y_2] 	[h_high] ...
                point 8 	[x_1] 	0 		[h_low] ...
                point 9 	0 		[-y_1] 	[h_low] ...
                point 10 	[x_1] 	0 		[h_high] ...
                point 11 	0 		[-y_1] 	[h_high] ...
                point 12 	[x_1] 	[-y_1] 	[h_low] ...
                point 13 	[x_1] 	[-y_1] 	[h_high] ...
                size 5 [int(h_high-h_low)] 5 2 ...
                dimension 0.5 0.5 ...
                group 'Block3' slot 'Block'

    zone reflect normal 0 1 0 origin 0 0 0 range position-z 0 100
    zone reflect normal 1 0 0 origin 0 0 0 range position-z 0 100

    ;zone export 'guoduduan.f3grid' binary
    ''')

    it.command('''
    structure shell create by-zone-face id 11 group 'palte_top' slot 'GuoDuDuan' range position-z [h_low]
    structure shell create by-zone-face id 11 group 'palte_top2' slot 'GuoDuDuan' range group 'Block1' slot 'Block' position-z [h_high]

    zone face group 'EmbPile_top' slot '1' internal range group 'Block1' slot 'Block' group 'Block2' slot 'Block' 
    zone separate by-face new-side group 'EmbPile_Side_top' slot '3' range group 'EmbPile_top' slot '1'
    structure liner create  by-face id 11 group 'guoduduan' slot 'GuoDuDuan' element-type=dkt-cst embedded range group 'EmbPile_Side_top' slot '3'

    zone delete range position-z 0 100
    structure node initialize position-z [h_high-1] range group 'guoduduan' slot 'GuoDuDuan' position-z [h_high-1-0.5] [h_high-1+0.5]
    ''')

    #
    v_temp = np.array([x_radial*np.sqrt(2)/2,x_radial*np.sqrt(2)/2,h_high-1])
    command1 = "structure beam create by-line {} {} id 11 group 'xiecheng' slot 'GuoDuDuan' segments 3 ".format(tuple(np.array(v1[0])*(1,1,0)+(0,0,H_list[0]+1)),tuple(v_temp*(1,1,1)))
    command2 = "structure beam create by-line {} {} id 11 group 'xiecheng' slot 'GuoDuDuan' segments 3 ".format(tuple(np.array(v1[0])*(-1,1,0)+(0,0,H_list[0]+1)),tuple(v_temp*(-1,1,1)))
    command3 = "structure beam create by-line {} {} id 11 group 'xiecheng' slot 'GuoDuDuan' segments 3 ".format(tuple(np.array(v1[0])*(1,-1,0)+(0,0,H_list[0]+1)),tuple(v_temp*(1,-1,1)))
    command4 = "structure beam create by-line {} {} id 11 group 'xiecheng' slot 'GuoDuDuan' segments 3 ".format(tuple(np.array(v1[0])*(-1,-1,0)+(0,0,H_list[0]+1)),tuple(v_temp*(-1,-1,1)))
    it.command(command1)
    it.command(command2)
    it.command(command3)
    it.command(command4)

    print("GuoDuDuan built!")
    
    #it.command("structure beam delete range group 'xietui' position-z 4.0 -4.5")

    it.command("structure node join")
    it.command("model save 'Jacket.sav'")

    print("'Jacket' saved!")

def Pipe_Property(diameter,thickness):
    section_area = np.pi * diameter**2 / 4 - np.pi * (diameter-thickness * 2)**2 / 4
    moi_y = np.pi * (diameter**4 - (diameter - thickness * 2)**4) / 64
    moi_polar = moi_y * 2
    return section_area, moi_y, moi_polar

def Density_Factor(mass_aimed,pos_z):
    it.command("model restore 'Jacket.sav'")
    command = '''
    structure shell property density 7.85 thickness 0.060 range group 'palte_top' slot 'GuoDuDuan'
    structure shell property density 0.00 thickness 0.150 range group 'palte_top2' slot 'GuoDuDuan'
    structure liner property density 7.85 thickness 0.180 range group 'guoduduan' slot 'GuoDuDuan'
    structure beam property density 7.85 cross-sectional-area=0.324 range group 'xiecheng' slot 'GuoDuDuan'
    structure beam property density 7.85 cross-sectional-area=0.324 range group 'zhutui' slot 'GuoDuDuan'
    structure liner delete range position-z {} -1000
    structure beam delete range position-z {} -1000
    '''.format(pos_z,pos_z)
    it.command(command)
    
    mass_liner = mass_beam = mass_shell = 0.
    
    for se in it.structure.list():
        if type(se) is it.structure.Liner:
            mass_liner = mass_liner + se.volume()*se.density()
        elif type(se) is it.structure.Beam:
            mass_beam = mass_beam + se.volume()*se.density()
        elif type(se) is it.structure.Shell:
            mass_shell = mass_shell + se.volume()*se.density()
    
    fac_density = mass_aimed / (mass_liner + mass_beam + mass_shell)
    print(fac_density)
    return fac_density

def Jacket_Property(fac_density,isotropic,zhutui,xietui,H_list):
    it.command("model restore 'Jacket.sav'")
    #general property
    it.command("structure beam property young = {} poisson = {}".format(isotropic[0],isotropic[1]))
    it.command("structure shell property isotropic {} {}".format(isotropic[0],isotropic[1]))
    it.command("structure liner property isotropic {} {}".format(isotropic[0],isotropic[1]))
    #GuoDuDuan property
    command = '''
    structure shell property density [7.85*{}] thickness 0.060 range group 'palte_top' slot 'GuoDuDuan'
    structure shell property density [0.00*{}] thickness 0.150 range group 'palte_top2' slot 'GuoDuDuan'
    structure liner property density [7.85*{}] thickness 0.180 range group 'guoduduan' slot 'GuoDuDuan'
    structure liner property coupling-stiffness-normal 2e8 coupling-stiffness-shear 2e8 coupling-yield-normal 1e6 coupling-cohesion-shear 2.5e3 coupling-friction-shear 50 range group 'guoduduan' slot 'GuoDuDuan'
    structure beam property density [7.85*{}] cross-sectional-area=0.324 moi-polar=0.087 moi-y=0.058 moi-z=0.029 range group 'xiecheng' slot 'GuoDuDuan'
    structure beam property density [7.85*{}] cross-sectional-area=0.324 moi-polar=0.087 moi-y=0.058 moi-z=0.029 range group 'zhutui' slot 'GuoDuDuan'
    '''.format(fac_density,fac_density,fac_density,fac_density,fac_density)
    it.command(command)
    #Jacket property
    prop_xietui = Pipe_Property(xietui[0],xietui[1])
    command = '''
    structure beam property density 7.85 cross-sectional-area={} moi-polar={} moi-y={} moi-z={} range group 'xietui' slot 'jacket'
    '''.format(prop_xietui[0],prop_xietui[2],prop_xietui[1],prop_xietui[1])
    it.command(command)
    #
    command = '''
    structure beam property density 7.85 cross-sectional-area={} moi-polar={} moi-y={} moi-z={} range position-z {} {} group 'zhutui' slot 'jacket'
    '''
    for i in range(len(H_list)-1):
        prop_zhutui = Pipe_Property(zhutui[i][0],zhutui[i][1])
        print(prop_zhutui)
        it.command(command.format(prop_zhutui[0],prop_zhutui[2],prop_zhutui[1],prop_zhutui[1],H_list[i],H_list[i+1]))
    
    #Lianjieduan property
    command = '''
    structure beam property density 7.85 young=2.1e8 poisson=0.30 cross-sectional-area=0.280 moi-polar=0.060 moi-y=0.030 moi-z=0.030 range group 'lianjieduan' slot 'jacket'
    '''
    it.command(command)

def SuctionBucket_main(mudline,L,scour_depth,thickness):   
    
    command = '''
    structure liner create by-zone-face id 11 group 'Cap' slot 'SC' element-type=dkt-cst range position-z {} group 'SC' slot 'suction caisson'
    zone face group 'InterFace' slot '1' internal range group 'NoSC' slot 'suction caisson' group 'SC' slot 'suction caisson' position-z {} {}
    zone separate by-face new-side group 'InterFace2' range group 'InterFace' slot '1'
    structure liner create by-face id 11 group 'Skirt' slot 'SC' element-type=dkt-cst embedded range group 'InterFace2'
    
    structure liner group 'bucket' range group 'Skirt' slot 'SC'
    structure liner group 'bucket' range group 'Cap' slot 'SC'
    '''.format(mudline,mudline-L,mudline)
    it.command(command)
    
    command = '''
    structure liner property isotropic 2.1e8 0.3
    structure liner property density 7.85 thickness {} range group 'Skirt' slot 'SC'
    structure liner property density 0.08 thickness 0.600 range group 'Cap' slot 'SC'
    structure node join
    '''.format(thickness)
    it.command(command)
    
    command = '''
    fish define Interaction
        loop foreach local _se struct.list(struct.group(::struct.list)=='bucket')
            struct.liner.normal.stiffness(_se,1)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            struct.liner.normal.stiffness(_se,2)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            struct.liner.shear.stiffness(_se,1)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            struct.liner.shear.stiffness(_se,2)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            local angle = zone.prop(zone.near(struct.pos(_se)),'friction')
            struct.liner.shear.friction(_se,1)=math.atan(math.tan(angle*math.pi/180)*0.8)/math.pi*180
            struct.liner.shear.friction(_se,2)=math.atan(math.tan(angle*math.pi/180)*0.8)/math.pi*180
            struct.liner.shear.cohesion(_se,1)=zone.prop(zone.near(struct.pos(_se)),'cohesion')*0.8
            struct.liner.shear.cohesion(_se,2)=zone.prop(zone.near(struct.pos(_se)),'cohesion')*0.8
        endloop
    end
    '''
    it.command(command)
    it.fish.call_function('Interaction')
    
    command ='''
    structure liner property slide off
    structure link tolerance-slide 1.5
    '''
    it.command(command)
    
    print("Suction Caisson built!")
    
    command1 ='''
    model solve ratio 1e-6
    model save 'StruProp.sav'
    '''
    
    command2 ='''
    zone delete range position-z {} {} group 'SC' slot 'suction caisson' not
    model solve ratio 1e-6
    model save 'StruProp.sav'
    '''.format(mudline,mudline-scour_depth)
    
    if scour_depth == 0:
        it.command(command1)
    else:
        it.command(command2)


