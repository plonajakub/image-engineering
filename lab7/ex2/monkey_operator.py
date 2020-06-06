import bpy

class AddMonkeyOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.add_monkey_operator"
    bl_label = "Custom Monkey"

    def execute(self, context):
        bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 0))
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.data.objects[-1].modifiers["Subdivision"].render_levels = 3
        bpy.data.objects[-1].modifiers["Subdivision"].levels = 3
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AddMonkeyOperator)


def unregister():
    bpy.utils.unregister_class(AddMonkeyOperator)


if __name__ == "__main__":
    register()
