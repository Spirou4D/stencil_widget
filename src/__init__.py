bl_info = {
    "name": "Stencil Widget",
    "description": "Show a widget to control the stencil brush",
    "author": "kgeogeo, Spirou4D",
    "version": (1, 2),
    "blender": (2, 7, 8),
    "location": "ctrl + shift +Q > Texture Stencil  OR shift + alt + Q > Mask Stencil",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Paint"}

import bpy
from . import stencil_widget, mask_stencil_widget

def register():
    bpy.utils.register_module(__name__)
    km_list = ['Image Paint', 'Sculpt', 'Vertex Paint']
    for i in km_list:
        km = bpy.context.window_manager.keyconfigs.default.keymaps[i]
        kmi = km.keymap_items.new("brush.stencil_widget", 'Q', 'PRESS', shift=True, ctrl=True)
        kmi = km.keymap_items.new("brush.mask_stencil_widget", 'Q', 'PRESS', shift=True, alt=True)

def unregister():
    km_list = ['Image Paint', 'Sculpt', 'Vertex Paint']
    for i in km_list:
        km = bpy.context.window_manager.keyconfigs.default.keymaps[i]
        for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"brush.mask_stencil_widget", }):
            km.keymap_items.remove(kmi)
        for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"brush.stencil_widget", }):
            km.keymap_items.remove(kmi)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
