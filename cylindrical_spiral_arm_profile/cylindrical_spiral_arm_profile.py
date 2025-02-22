# Author-
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def cosec(angle):
    return 1 / math.sin(angle)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        
        # Parameters (all values in mm)
        num_sections = 20  # Approximate number of sections from the image
        base_width = 2.0  # Base width of each section in mm
        rise_factor = 1.05  # Progressive growth factor for rise
        flat_length = 2.0  # Flat section length in mm
        height_initial = 3.0  # Initial height in mm
        rise_angle = math.radians(90 - 6.666)  # Rising angle in degrees converted to radians
        fall_angle = math.radians(90 - 23.3333)  # Falling angle in degrees converted to radians
        rotation_angle = math.radians(5)  # Overall rotation in degrees converted to radians
        
        # Create a new sketch
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        lines = sketch.sketchCurves.sketchLines
        
        # Starting point (in mm)
        x, y = 0.0, 0.0
        prev_point = adsk.core.Point3D.create(x, y, 0)
        
        for i in range(num_sections):
            # Compute rise and fall distances progressively (in mm)
            rise_length = height_initial * (rise_factor ** i) * cosec(rise_angle)
            fall_length = height_initial * (rise_factor ** i) * cosec(fall_angle)
            
            # Rising segment (in mm)
            x += rise_length * math.cos(rise_angle)
            y += rise_length * math.sin(rise_angle)
            rise_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, rise_point)
            prev_point = rise_point
            
            # Flat segment (kept horizontal in mm)
            x += flat_length
            flat_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, flat_point)
            prev_point = flat_point
            
            # Falling segment (in mm)
            x += fall_length * math.cos(fall_angle)
            y -= fall_length * math.sin(fall_angle)
            fall_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, fall_point)
            prev_point = fall_point
        
        # Elastic axis (in mm)
        elastic_start = adsk.core.Point3D.create(0.0, -0.5, 0)
        elastic_end = adsk.core.Point3D.create(x, -0.5, 0)
        lines.addByTwoPoints(elastic_start, elastic_end)
        
        # Apply rotation (in radians)
        transform = adsk.core.Matrix3D.create()
        transform.setToRotation(rotation_angle, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
        sketch.transform(transform)
        
        ui.messageBox('Elastic axis profile corrected and generated with units in mm!')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
