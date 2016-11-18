import bpy, bgl, blf, sys, os
from math import *
from mathutils import *

############################################## Parameters  ####################################################
tab_size = [15,100,135]
tab_nb_seg = [16,4]
nb_part = 11
ec = 3

key_list = ['NUMPAD_0', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_5', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_PERIOD', 'PERIOD']
key_sign = ['NUMPAD_MINUS', 'MINUS']
tab_first_time = []

############################################## Widget drawing  #################################################
def draw_callback_px(self, context):

    #Init
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)

    if not self.intuitive_scale:
        #manipulator
        bgl.glPushMatrix()
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glTranslatef(self.center.x,self.center.y,0)
        bgl.glRotatef(degrees(self.draw_angle),0,0,1)

        bgl.glPointSize(2)
        bgl.glBegin(bgl.GL_POINTS)
        bgl.glVertex2f(0,0)
        bgl.glEnd()
        bgl.glPointSize(1)

        c = []
        s = []
        for i in range(tab_nb_seg[0]):
            c.append(cos(i*pi/(tab_nb_seg[0]/2)))
            s.append(sin(i*pi/(tab_nb_seg[0]/2)))

        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)

        bgl.glBegin(bgl.GL_LINE_LOOP)
        for i in range(tab_nb_seg[0]):
            bgl.glVertex2f(tab_size[0]*c[i], tab_size[0]*s[i])
        bgl.glEnd()

        c = []
        s = []

        for i in range(tab_nb_seg[1]+1):
            c.append(cos(i*(pi/((nb_part) * tab_nb_seg[1]/2) - radians(ec)/2) + pi/2 + radians(ec)))
            s.append(sin(i*(pi/((nb_part) * tab_nb_seg[1]/2) - radians(ec)/2) + pi/2 + radians(ec)))

        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)

        for i in range(nb_part):

            bgl.glPushMatrix()
            bgl.glRotatef(i*360/nb_part,0,0,1)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for j in range(tab_nb_seg[1]+1):
                bgl.glVertex2f(tab_size[1]*c[j], tab_size[1]*s[j])
            bgl.glEnd()
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for j in range(tab_nb_seg[1]+1):
                bgl.glVertex2f(tab_size[2]*c[j], tab_size[2]*s[j])
            bgl.glEnd()
            bgl.glPopMatrix()

            bgl.glPushMatrix()
            bgl.glRotatef(i*360/nb_part - ec,0,0,1)
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(0,tab_size[1])
            bgl.glVertex2f(0,tab_size[2])
            bgl.glEnd()
            bgl.glPopMatrix()
            bgl.glPushMatrix()
            bgl.glRotatef(i*360/nb_part + ec,0,0,1)
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(0,tab_size[1])
            bgl.glVertex2f(0,tab_size[2])
            bgl.glEnd()
            bgl.glPopMatrix()

        bgl.glDisable(bgl.GL_LINE_SMOOTH)

        bgl.glEnable(bgl.GL_TEXTURE_2D)
        for i in range(nb_part):
            img = bpy.data.images[self.icons[i]]
            img.gl_load(bgl.GL_NEAREST, bgl.GL_NEAREST)
            # 2.77 API change
            if bpy.app.version >= (2, 77, 0):
                texture1 = img.bindcode[0]
            else:
                texture1 = img.bindcode
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture1);
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_LINEAR)
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_LINEAR)

            bgl.glPushMatrix()
            bgl.glRotatef(-360/(2*nb_part) - i*360/nb_part,0,0,1)
            bgl.glTranslatef(0, (tab_size[1] + tab_size[2])/2,0)
            bgl.glBegin(bgl.GL_QUADS)
            bgl.glTexCoord2d(0,0)
            bgl.glVertex2f(-15, -15)
            bgl.glTexCoord2d(0,1)
            bgl.glVertex2f(-15, 15)
            bgl.glTexCoord2d(1,1)
            bgl.glVertex2f(15, 15)
            bgl.glTexCoord2d(1,0)
            bgl.glVertex2f(15, -15)
            bgl.glEnd()
            bgl.glPopMatrix()
        bgl.glDisable(bgl.GL_TEXTURE_2D)
        bgl.glPopMatrix()

        if self.draw_angle != 0:
            font_id = 0
            blf.size(font_id, 20, 72)
            blf.position(font_id, self.center.x - blf.dimensions(font_id,self.bfl_print[0])[0]/2, self.center.y + 5 + tab_size[0], 0)
            blf.draw(font_id, self.bfl_print[0])
            blf.position(font_id, self.center.x - blf.dimensions(font_id,self.bfl_print[1])[0]/2, self.center.y - 5 - tab_size[0]-blf.dimensions(font_id,self.bfl_print[1])[1], 0)
            blf.draw(font_id, self.bfl_print[1])
    else:
        bgl.glEnable(bgl.GL_POINT_SMOOTH)
        bgl.glPointSize(5)
        if len(self.tab_point) >=2:
            bgl.glColor4f(1.0, 0.0, 0.0, 1.0)
            bgl.glBegin(bgl.GL_POINTS)
            bgl.glVertex2f(self.tab_point[0].x, self.tab_point[0].y)
            bgl.glVertex2f(self.tab_point[1].x, self.tab_point[1].y)
            bgl.glEnd()
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(self.tab_point[0].x, self.tab_point[0].y)
            bgl.glVertex2f(self.tab_point[1].x, self.tab_point[1].y)
            bgl.glEnd()
        if len(self.tab_point) == 4:
            bgl.glColor4f(0.0, 0.0, 1.0, 1.0)
            bgl.glBegin(bgl.GL_POINTS)
            bgl.glVertex2f(self.tab_point[2].x, self.tab_point[2].y)
            bgl.glVertex2f(self.tab_point[3].x, self.tab_point[3].y)
            bgl.glEnd()
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(self.tab_point[2].x, self.tab_point[2].y)
            bgl.glVertex2f(self.tab_point[3].x, self.tab_point[3].y)
            bgl.glEnd()

    #reinit value
    bgl.glDisable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(1)
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

##############################################   Action ########################################################
def widget_action(self, context, event, brush):
    vec_act = Vector((event.mouse_region_x,event.mouse_region_y)) - self.first_mouse
    reinit_fm = True

    # cercle du milieu
    if self.center_dist <= tab_size[0]:
        self.center += vec_act  # modifie le centre du widget par celui du clic-souris
        # et change l'origine de la texture pourles rotations futurs!
        self.origine -= div_v2v2(rotate_point(vec_act,-degrees(brush.texture_slot.angle)),self.scale)

    # entre les deux cercles
    if tab_size[0] <  self.center_dist <= tab_size[1]:
        self.center += vec_act          # chgt du centre du widget
        brush.stencil_pos += vec_act    # donc deplacement du stencil

    # cercle des boutons
    if tab_size[1] < self.center_dist <= tab_size[2]:
        vec_init = self.first_mouse - self.center   # deplace le vecteur initial  au centre du widget
        vec_rot =  Vector((event.mouse_region_x,event.mouse_region_y)) - self.center # creer un vecteur qui tourne sur le widget
        man_angle = vec_rot.angle_signed(vec_init)  # angle entre vecteur initial et le vecteur qui tourne

        center_dist = (Vector((event.mouse_region_x,event.mouse_region_y))-self.center).length # longueur du vecteur tournant
        if center_dist > tab_size[2] and abs(degrees(man_angle)) < 5:
            man_angle = 0
            reinit_fm = False
        elif center_dist > tab_size[2] and abs(degrees(man_angle)) > 5:
            sign = -1 if man_angle < 0 else 1
            man_angle = sign * radians(5)

        self.draw_angle += man_angle

        if self.part == 0: #Rotation
            final_angle = (brush.texture_slot.angle + man_angle) # raisonnement bizarre!!!
            final_angle %=2*pi                                 # clampage selon les radians
            brush.texture_slot.angle = final_angle            # applique la rotation

        if self.part == 1:                  # Echelle Stencil XY
            self.scale *= 1+man_angle
        if self.part == 2:                  # Echelle Stencil selon X
            self.scale.x *= 1+man_angle
        if self.part == 3:                  # Echelle Stencil selon Y
            self.scale.y *= 1+man_angle

        self.scale = clamp_v(0.01, self.scale, 50)    # clampage de la mise à l'echelle max
        brush.stencil_dimension = mul_v2v2(self.img_size, self.scale)   # changement de la dimension du stencil aussi!

        if self.part == 4 :                 # Echelle Texture selon XY
            brush.texture_slot.scale =  Vector((brush.texture_slot.scale.x*(1+man_angle), brush.texture_slot.scale.y*(1+man_angle), 1.0))
        if self.part == 5:                  # Echelle Texture selon X
            brush.texture_slot.scale =  Vector((brush.texture_slot.scale.x*(1+man_angle), brush.texture_slot.scale.y, 1.0))
        if self.part == 6:                  # Echelle Texture selon Y
            brush.texture_slot.scale =  Vector((brush.texture_slot.scale.x, brush.texture_slot.scale.y*(1+man_angle), 1.0))

        brush.texture_slot.scale = clamp_v(0.1,brush.texture_slot.scale,100).to_3d() #chgt de l'echelle de la texture

        if self.part == 7:                 # Decalage texture selon X
            brush.texture_slot.offset -=  Vector((man_angle, 0, 0.0))
        if self.part == 8:                 # Decalage texture selon Y
            brush.texture_slot.offset -=  Vector((0, man_angle, 0.0))

        brush.texture_slot.offset = clamp_v(-10,brush.texture_slot.offset,10).to_3d() # chgt du décalage de la texture

        if self.part == 9:                # Opacité
            brush.texture_overlay_alpha -= degrees(man_angle)
            brush.texture_overlay_alpha = clamp(0, brush.texture_overlay_alpha, 50)  # Chgt de l'opacité clampée

        print_action_value(self, context, brush)      # ecriture des infos dans le widget

    if reinit_fm:                #Re-initiation si fin du mouvement souris
            self.first_mouse = Vector((event.mouse_region_x,event.mouse_region_y))   # Chgt du clic-départ de la souris

################################################ Action Numpad #################################################
def widget_action_numpad(self, context, event, brush):
    func_key_val(self, context, event)
    if float(self.key_val) != 0:
        if self.first_key_val:
            self.first_mouse = Vector((event.mouse_region_x,event.mouse_region_y))
            self.center_dist = (self.first_mouse-self.center).length
            self.part = find_part(self)
            self.first_key_val = False

            self.init_angle = brush.texture_slot.angle
            self.init_scale = self.scale.copy()
            self.init_uvscale = brush.texture_slot.scale.copy()
            self.uvoffset = brush.texture_slot.offset.copy()
            self.alpha = brush.texture_overlay_alpha

        self.draw_angle = 0.00001

        if self.part == 0: #Rotation
            final_angle = self.init_angle + radians(float(self.key_val))
            final_angle %=2*pi
            brush.texture_slot.angle =  final_angle

        if self.part == 1 :
            self.scale = self.init_scale * float(self.key_val)
        if self.part == 2:
            self.scale.x = self.init_scale.x * float(self.key_val)
        if self.part == 3:
            self.scale.y = self.init_scale.y * float(self.key_val)

        self.scale = clamp_v(0.01, self.scale, 50)
        brush.stencil_dimension = mul_v2v2(self.img_size, self.scale)

        if self.part == 4 :
            brush.texture_slot.scale =  Vector((self.init_uvscale.x*float(self.key_val), self.init_uvscale.y*float(self.key_val), 1.0))
        if self.part == 5:
            brush.texture_slot.scale =  Vector((self.init_uvscale.x*float(self.key_val), self.init_uvscale.y, 1.0))
        if self.part == 6:
            brush.texture_slot.scale =  Vector((self.init_uvscale.x, self.init_uvscale.y*float(self.key_val), 1.0))

        brush.texture_slot.scale = clamp_v(0.1,brush.texture_slot.scale,100).to_3d()

        if self.part == 7:
            brush.texture_slot.offset = self.uvoffset + Vector((float(self.key_val), 0, 0.0))
        if self.part == 8:
            brush.texture_slot.offset = self.uvoffset + Vector((0, float(self.key_val), 0.0))

        brush.texture_slot.offset = clamp_v(-10,brush.texture_slot.offset,10).to_3d()

        if self.part == 9: #Opacity
            brush.texture_overlay_alpha = self.alpha + float(self.key_val)
            brush.texture_overlay_alpha = clamp(0, brush.texture_overlay_alpha, 50)

        print_action_value(self, context, brush)

################################################ Clear the value   #############################################
def clear_value(self, context, event, brush):
    self.first_mouse = Vector((event.mouse_region_x,event.mouse_region_y))
    self.center_dist = (self.first_mouse-self.center).length

    if self.center_dist <= tab_size[0]:
        self.center = Vector((brush.stencil_pos.x, brush.stencil_pos.y))
        self.origine = Vector((0,0))

    if tab_size[0] <  self.center_dist <= tab_size[1]:
        self.center = Vector((context.area.width/2,context.area.height/2))

    if tab_size[1] < self.center_dist <= tab_size[2]:
        self.part = find_part(self)

        if self.part == 0:
            brush.texture_slot.angle = 0

        if self.part == 1:
            self.scale = Vector((1,1))
        if self.part == 2:
            self.scale.x = 1
        if self.part == 3:
            self.scale.y = 1
        brush.stencil_dimension = mul_v2v2(self.img_size, self.scale)

        if self.part == 4:
            brush.texture_slot.scale =  Vector((1, 1, 1))
        if self.part == 5:
            brush.texture_slot.scale =  Vector((1, brush.texture_slot.scale.y, 1))
        if self.part == 6:
            brush.texture_slot.scale =  Vector((brush.texture_slot.scale.x, 1, 1))

        if self.part in [7] :
            brush.texture_slot.offset =  Vector((0, brush.texture_slot.offset.y, 0))
        if self.part in [8] :
            brush.texture_slot.offset =  Vector((brush.texture_slot.offset.x, 0, 0))

        if self.part == 9:
            brush.texture_overlay_alpha = 50

######################################## Print value ###########################################################
def print_action_value(self, context, brush):
    if self.part == 0:
        self.bfl_print = ["Rotation", '%.1f' % degrees(brush.texture_slot.angle) + '°']
    if self.part == 1:
        self.bfl_print = ["Scale", ('%.2f' % (self.scale.x)) + ' , ' + ('%.2f' % (self.scale.y))]
    if self.part == 2:
        self.bfl_print = ["Scale X", '%.2f' % self.scale.x]
    if self.part == 3:
        self.bfl_print = ["Scale y", '%.2f' % self.scale.y]
    if self.part == 4 :
        self.bfl_print = ["Scale UV", ('%.2f' % brush.texture_slot.scale.x) + ' , ' + ('%.2f' % brush.texture_slot.scale.y)]
    if self.part == 5:
        self.bfl_print = ["Scale UV X", '%.2f' % brush.texture_slot.scale.x]
    if self.part == 6:
        self.bfl_print = ["Scale UV Y", '%.2f' % brush.texture_slot.scale.y]
    if self.part == 7:
        self.bfl_print = ["Offset UV X", '%.2f' % brush.texture_slot.offset.x]
    if self.part == 8:
        self.bfl_print = ["Offset UV Y", '%.2f' % brush.texture_slot.offset.y]
    if self.part == 9:
        self.bfl_print = ["Opacity", ('%.0f' % brush.texture_overlay_alpha) + "%"]

######################################  Usefull Function   #####################################################

def rotate_point(p, angle):
    s = sin(radians(angle));
    c = cos(radians(angle));
    v = Vector((p.x * c - p.y * s, p.x * s + p.y * c))
    return v

def find_part(self):
    up_vec = Vector((0,1))
    init_vec = self.first_mouse - self.center
    part = degrees(up_vec.angle_signed(init_vec))/(360/nb_part)
    sign = 0
    if abs(part)!=0:
        sign = part/abs(part)
    if sign < 0:
        part = nb_part-abs(part)
    return trunc(part)


def load_icon():
    tmp_path = ''

    for path in sys.path:
        if path.endswith("addons"):
            if path.count('/') > 0:
                slash = '/'
            else:
                slash = '\\'
            path = path + slash + "stencil_widget" + slash
            if os.path.exists(path):
                tmp_path = path

    icons = []
    if tmp_path:
        path = tmp_path + slash + "icon" + slash
        for i in range(1, nb_part+1):
            try:
                #print(path + str(i) + ".png")
                bpy.data.images.load(path + str(i) + ".png")
                icons.append(str(i) + ".png")
            except:
                print('Erreur Icons')
    else:
        print("Don't find the icon")

    return icons

def remove_icon(icons):
        for img in icons:
            bpy.data.images[img].user_clear()
            bpy.data.images.remove(bpy.data.images[img])

def func_key_val(self, context, event):
    if event.type in  key_list:
        if event.type in ['NUMPAD_PERIOD', 'PERIOD']:
            c = '.' if self.key_val.count('.') == 0 else ''
        else:
            c = event.type[7]
        self.key_val += c

    if event.type in key_sign:
        self.key_val = self.key_val.replace('+','-') if self.key_val[0] == '+' else self.key_val.replace('-','+')

def find_brush(context):
    tool_settings = context.tool_settings
    if context.mode == 'SCULPT':
        return tool_settings.sculpt.brush
    elif context.mode == 'PAINT_TEXTURE':
        return tool_settings.image_paint.brush
    elif context.mode == 'PAINT_VERTEX':
        return tool_settings.vertex_paint.brush
    else:
        return None

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def clamp_v(minimum, v, maximum):
    return Vector((clamp(minimum, v.x, maximum), clamp(minimum, v.y, maximum)))

def mul_v2v2(v1,v2):                  # multiplication de vecteurs
    return Vector((v1.x * v2.x, v1.y * v2.y))

def div_v2v2(v1,v2):                  # divisin de vecteurs
    return Vector((v1.x / v2.x, v1.y / v2.y))


#####################################################   Main Class ################################################
class Stencil_Widget(bpy.types.Operator):
    bl_idname = "brush.stencil_widget"
    bl_label = "Stencil Widget"

    _handle_draw = None
    lmb = False                       # clic bouton gauche

    origine = Vector((0,0))           # REPERE
    center = Vector((-1,-1))          # centre x & y

    center_dist = 0                   # distance au centre
    draw_angle = 0                    # angle
    value = []                        # valeurs
    img_size = Vector((256,256))      # Taille x & y Mask
    scale = Vector((1,1))             # zoom x & y
    icons = []                        # tableau d'icone

    tab_point = []                    # tableau de points

    key_val = '+0'
    first_key_val = True
    intuitive_scale = False           # si on ne affiche pas la texture

    @classmethod
    def poll(cls, context):
        brush = find_brush(context)
        return context.region.type == 'WINDOW' and brush.texture_slot.texture

    def modal(self, context, event):
        context.area.tag_redraw()
        brush = find_brush(context)
        exit = False # si le curseur-souris est hors du widget

        if not self.intuitive_scale:                       # use of buttons
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                # Enregistrement du premier clic souris!
                self.first_mouse = Vector((event.mouse_region_x,event.mouse_region_y))
                # distance du clic-souris au centre du widget
                self.center_dist = (self.first_mouse-self.center).length

                if self.center_dist > tab_size[2] + 10:
                    exit = True # click hors widget

                self.part = find_part(self) # debut de l'action bouton

                if self.part == 10: # click to pass in intuitive mode
                    self.intuitive_scale = True

                self.key_val = '+0'
                first_key_val = True           # memorise le clic touche
                self.lmb = True                # memorise le clic gauche

            if event.type == 'MOUSEMOVE' and self.lmb:
                widget_action(self, context, event, brush)    #le mouvement de souris lance les functions boutons du widget

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self.draw_angle = 0
                self.lmb = False     # fin du clic deplt du clic-souris

            # s'il ne s'agit que de touches-claviers de chiffres!
            if event.type in (key_list + key_sign) and event.value == 'PRESS':
                widget_action_numpad(self, context, event, brush)

            # s'il s'agit de la touche d'entrer de fonctions
            if event.type in ['RET', 'NUMPAD_ENTER'] and event.value == 'PRESS':
                self.key_val = '+0'
                self.draw_angle = 0
                self.first_key_val = True        # memorise le clic touche

            # s'il s'agit de la touche C
            # réintie les valeurs par défaut
            if event.type == 'C' and event.value == 'PRESS':
                clear_value(self, context, event, brush)
        else:                                               # Scale Intuitive mode
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                self.lmb = True          #clic bouton gauche souris
                # ajoute positions du clic souris de départ + clic arrivée temporaire
                self.tab_point.append(Vector((event.mouse_region_x,event.mouse_region_y)))
                # ajoute positions du clic arrivée temporaire donc tab_point possède deux points
                self.tab_point.append(Vector((event.mouse_region_x,event.mouse_region_y)))

            if event.type == 'MOUSEMOVE' and self.lmb: #clic-souris tournant autour du centre
                if len(self.tab_point) == 2: #s'il y a deux clic-souris, chgt du 2e
                    self.tab_point[1] = Vector((event.mouse_region_x,event.mouse_region_y))
                if len(self.tab_point) == 4: #s'il y a quatre clic-souris, chgt du 4e
                    self.tab_point[3] = Vector((event.mouse_region_x,event.mouse_region_y))

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self.lmb = False # fin de l'enregistrement souris par la "RELEASE"
                if len(self.tab_point) >= 4:                    # si 4 points ou plus
                    v1 = self.tab_point[1] - self.tab_point[0]
                    v2 = self.tab_point[3] - self.tab_point[2]
                    if v2.x != 0:
                        # modif de la proportion selon x
                        propx =   v1.x/v2.x          # Proportion selon X
                        self.scale *= abs(propx)     # chgt de l'echelle selon x de l'image
                        brush.stencil_dimension *= abs(propx) # Echelle du stencil selon propx

                        self.tab_point = []       # on vide les points de clics
                        self.intuitive_scale = False  # on stope la mise à l'echelle intuitive
                    else:
                        print('You must draw two lines with your cursor, please')

        # chgt de la position du stencil
        # position x/y du centre de l'ecran
        brush.stencil_pos = self.center + rotate_point(mul_v2v2(self.origine,self.scale), degrees(brush.texture_slot.angle))

        ret = 'RUNNING_MODAL'

        if event.type in ['RIGHTMOUSE','Q'] and event.value == 'PRESS' or exit:
            global tab_first_time
            for i in range(len(tab_first_time)):
                if tab_first_time[i][0] == brush:
                    tab_first_time[i][1] = Vector((brush.stencil_pos.x,brush.stencil_pos.y)) - self.center
                    tab_first_time[i][2] = degrees(brush.texture_slot.angle)
                    tab_first_time[i][3] = self.scale
            remove_icon(self.icons)
            self.tab_point = []
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_draw, 'WINDOW')
            ret = 'FINISHED'

        return {ret}

    def invoke(self, context, event):
        brush = find_brush(context)
        brush.texture_overlay_alpha = clamp(0, brush.texture_overlay_alpha, 50)

        try:
            ratio = brush.texture_slot.texture.image.size[1]/brush.texture_slot.texture.image.size[0]
            self.img_size = Vector((256,256*ratio))
        except:
            self.img_size = Vector((256, 256))

        self.scale = Vector((brush.stencil_dimension.x/self.img_size.x,brush.stencil_dimension.y/self.img_size.y))

        global tab_first_time
        first_time = True
        for b, c, a, s in tab_first_time:
            if b == brush:
                self.center = Vector((brush.stencil_pos.x,brush.stencil_pos.y)) - mul_v2v2(rotate_point(c, degrees(brush.texture_slot.angle) - a), div_v2v2(self.scale,s))
                first_time = False

        if first_time:
            self.center = Vector((brush.stencil_pos.x,brush.stencil_pos.y))
            self.origine = Vector((0,0))

            tab_first_time.append([brush,Vector((brush.stencil_pos.x,brush.stencil_pos.y)),degrees(brush.texture_slot.angle),self.scale])
        else:
            self.origine = div_v2v2(rotate_point(Vector((brush.stencil_pos.x,brush.stencil_pos.y)) - self.center, -degrees(brush.texture_slot.angle)), self.scale)

        self.icons = load_icon()
        self.tab_point = []

        args = (self, context)
        self._handle_draw = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
