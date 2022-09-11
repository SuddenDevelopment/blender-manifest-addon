import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Manifest",
    "author": "Anthony Aragues",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Tool Shelf > Tool",
    "description": "mesh instance count with dimensions",
    "warning": "",
    "doc_url": "https://github.com/SuddenDevelopment/blender-manifest-addon",
    "category": "3D View",
}

# sortby, set units
# Mesh name, x,y,z, instance count


def sortManifest(self, context):
    return sorted(context.scene.Manifest, key=lambda o: o[context.scene.Manifest_Sort])


def getSelectedObjects(context, type=None):
    arrObjects = context.selected_objects
    if len(context.selected_objects) == 0:
        arrObjects = context.scene.objects
    # filter by type
    if type is not None:
        arrObjects = [obj for obj in arrObjects if obj.type == type]
    return arrObjects


def getManifest(self, context):
    scene = context.scene
    scene.Manifest.clear()
    arrSelected = getSelectedObjects(context, "MESH")
    for obj in arrSelected:
        isNew = True
        objNewMesh = {
            "name": obj.data.name,
            "x": bpy.utils.units.to_string(
                scene.unit_settings.system,
                "LENGTH",
                obj.dimensions.x * obj.scale[0]),
            "y": bpy.utils.units.to_string(
                scene.unit_settings.system,
                "LENGTH",
                obj.dimensions.y * obj.scale[1]),
            "z": bpy.utils.units.to_string(
                scene.unit_settings.system,
                "LENGTH",
                obj.dimensions.z * obj.scale[2])
        }
        for objMesh in context.scene.Manifest:
            if objNewMesh["name"] == objMesh.name and objNewMesh["x"] == objMesh.x and objNewMesh["y"] == objMesh.y and objNewMesh["z"] == objMesh.z:
                isNew = False
                objMesh.count += 1
        if isNew == True:
            objAddMesh = context.scene.Manifest.add()
            objAddMesh.name = objNewMesh["name"]
            objAddMesh.x = objNewMesh["x"]
            objAddMesh.y = objNewMesh["y"]
            objAddMesh.z = objNewMesh["z"]
            objAddMesh.count = 1


class MANIFEST_MeshList(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")
    x: bpy.props.StringProperty(name="X", default="")
    y: bpy.props.StringProperty(name="Y", default="")
    z: bpy.props.StringProperty(name="Z", default="")
    count: bpy.props.IntProperty(name="Count", default=1)


class MANIFEST_OT_Load(bpy.types.Operator):
    """Create a Key for the current object, type of ket is determined by what you edit"""
    bl_idname = "manifest.load"
    bl_label = "Load manifest"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getManifest(self, context)
        return {'FINISHED'}


class MANIFEST_PT_Main(bpy.types.Panel):
    bl_label = "Manifest"
    bl_category = "Tool"
    bl_idname = "MANIFEST_PT_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # create the panel

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("manifest.load")
        row.prop(context.scene, "Manifest_Sort")
        row = layout.row()
        col_name = row.column(align=True)
        col_name.label(text="NAME")
        col_x = row.column(align=True)
        col_x.label(text="X")
        col_y = row.column(align=True)
        col_y.label(text="Y")
        col_z = row.column(align=True)
        col_z.label(text="Z")
        col_count = row.column(align=True)
        col_count.label(text="COUNT")
        for index, objMesh in enumerate(sortManifest(self, context)):
            col_value = col_name.row()
            col_value.label(text=objMesh.name)
            col_value = col_x.row()
            col_value.label(text=objMesh.x)
            col_value = col_y.row()
            col_value.label(text=objMesh.y)
            col_value = col_z.row()
            col_value.label(text=objMesh.z)
            col_value = col_count.row()
            col_value.label(text=str(objMesh.count))


arrClasses = [
    MANIFEST_PT_Main,
    MANIFEST_OT_Load,
    MANIFEST_MeshList,
]


def register():
    for i in arrClasses:
        bpy.utils.register_class(i)
    bpy.types.Scene.Manifest = bpy.props.CollectionProperty(
        type=MANIFEST_MeshList)
    bpy.types.Scene.Manifest_Sort = bpy.props.EnumProperty(
        name="sort",
        items=[
            ("name", "name", "sort manifest"),
            ("x", "x", "sort manifest"),
            ("y", "y", "sort manifest"),
            ("z", "z", "sort manifest"),
            ("count", "count", "sort manifest"),
        ],
        default="name"
    )


def unregister():
    for i in arrClasses:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.Manifest
    del bpy.types.Scene.Manifest_Sort
