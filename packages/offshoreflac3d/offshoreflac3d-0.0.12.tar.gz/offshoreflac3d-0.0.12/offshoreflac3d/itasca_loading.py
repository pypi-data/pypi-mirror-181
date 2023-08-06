import numpy as np
import itasca as it
it.command("python-reset-state false")

def define_reference_load_pos(h_high):
    it.command("model restore 'StruProp.sav'")
    command = '''
    structure node group 'loading_ref' slot 'reference' range position-z {} group 'guoduduan' slot 'GuoDuDuan'
    structure node history displacement-x position 0 0 {}
    structure node history displacement-y position 0 0 {}
    structure node history displacement-z position 0 0 {}
    structure node history velocity-x position 0 0 {}
    structure node history velocity-y position 0 0 {}
    structure node history velocity-z position 0 0 {}
    '''.format(h_high,h_high,h_high,h_high,h_high,h_high,h_high)
    it.command(command)

#0 for Fx, 1 for Fy, 2 for Fz, 3 for Mx, 4 for My, 5 for Mz

def loading_main(group,load,Type):
    Jx = Jy = Jp = 0
    Node_ref = []
    N = 0
    for sn in it.structure.node.list():
        if sn.group('reference') == group:
            Jx = Jx + sn.pos()[0]**2
            Jy = Jx
            Jp = Jx + Jy
            Node_ref.append(sn)
            N = N + 1
    
    load_n = load / N
    
    for sn_ref in Node_ref:
        if Type == 0:
            sn_ref.set_apply(Type,load_n)
        elif Type == 1:
            sn_ref.set_apply(Type,load_n)
        elif Type == 2:
            sn_ref.set_apply(Type,load_n)
        elif Type == 3:
            load_n = load*sn_ref.pos()[1]/Jx
            sn_ref.set_apply(Type-1,load_n)
        elif Type == 4:
            load_n = -load*sn_ref.pos()[0]/Jy
            sn_ref.set_apply(Type-2,load_n)
        elif Type == 5:
            r = np.sqrt(sn_ref.pos()[0]**2+sn_ref.pos()[1]**2)
            theta = np.arcsin(sn_ref.pos()[1]/r)
            load_n = load*r/Jy
            if sn_ref.pos()[0] < 0:
                sn_ref.set_apply(Type-5,-load_n*np.sin(theta))
                sn_ref.set_apply(Type-4,-load_n*np.cos(theta))
            else:
                sn_ref.set_apply(Type-5,-load_n*np.sin(theta))
                sn_ref.set_apply(Type-4, load_n*np.cos(theta))

# loading('loading_ref', 1000, 0)
# loading('loading_ref', 1000, 1)
# loading('loading_ref', 1000, 2)
# loading('loading_ref', 1000, 5)


# Horizontal for horizontal direction, Diagonal for diagnoal direction

def loading_ice(load,pos_z,direction):
    load_n = load / 4.
    command = '''
    structure node group 'loading_ref_ice' slot 'reference' range position-z {} group 'zhutui' slot 'jacket'
    '''.format(pos_z)
    it.command(command)
    
    if direction == 'Horizontal':
        command = '''
        structure node apply force {} 0 0 range group 'loading_ref_ice' slot 'reference'
        '''.format(load_n)
        it.command(command)
    elif direction == 'Diagonal':
        command = '''
        structure node apply force {} {} 0 range group 'loading_ref_ice' slot 'reference'
        '''.format(load_n*np.sqrt(2),load_n*np.sqrt(2))
        it.command(command)

#Loading_ice(1000,4.0,2)












