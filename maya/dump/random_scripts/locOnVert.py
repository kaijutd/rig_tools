import maya.api.OpenMaya as om2


def get_selected_vertices():
    sel = om2.MGlobal.getActiveSelectionList()

    if sel.length() == 0:
        raise RuntimeError("Nothing selected.")

    dagPath, component = sel.getComponent(0)

    if component.isNull():
        raise RuntimeError("Please select vertices (component mode).")

    if component.apiType() != om2.MFn.kMeshVertComponent:
        raise RuntimeError("Selection is not a vertex component.")

    compFn = om2.MFnSingleIndexedComponent(component)
    indices = compFn.getElements()

    return dagPath, indices


def build_matrix_from_normal(position, normal):
    normal = normal.normal()
    up = om2.MVector(0, 1, 0)
    if abs(normal * up) > 0.99:
        up = om2.MVector(1, 0, 0)

    tangent = (up ^ normal).normal()
    bitangent = (normal ^ tangent).normal()

    return om2.MMatrix((
        tangent.x, tangent.y, tangent.z, 0,
        bitangent.x, bitangent.y, bitangent.z, 0,
        normal.x, normal.y, normal.z, 0,
        position.x, position.y, position.z, 1
    ))


def create_locator(name, matrix, scale=0.1):
    dagMod = om2.MDagModifier()
    locObj = dagMod.createNode("locator")
    dagMod.doIt()

    dagPath = om2.MDagPath.getAPathTo(locObj)
    transformFn = om2.MFnTransform(dagPath)

    transformFn.setTransformation(om2.MTransformationMatrix(matrix))
    transformFn.setName(name)

    shapePath = dagPath.extendToShape()
    shapeFn = om2.MFnDependencyNode(shapePath.node())

    shapeFn.findPlug("localScaleX", False).setFloat(scale)
    shapeFn.findPlug("localScaleY", False).setFloat(scale)
    shapeFn.findPlug("localScaleZ", False).setFloat(scale)


def create_locators_on_vertices():
    dagPath, indices = get_selected_vertices()
    meshFn = om2.MFnMesh(dagPath)

    for i in indices:
        pos = meshFn.getPoint(i, om2.MSpace.kWorld)
        normal = meshFn.getVertexNormal(i, True, om2.MSpace.kWorld)

        matrix = build_matrix_from_normal(pos, normal)

        name = f"vtx_{i}_LOC"
        create_locator(name, matrix)

    print(f"Created {len(indices)} locator(s).")

create_locators_on_vertices()