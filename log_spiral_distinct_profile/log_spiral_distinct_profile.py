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
        
        # Parameters (all values in cm)
        num_sections = 35  # Approximate number of sections
        rise_factor = 1.05
        flat_length_initial = 0.78 * 0.15  # 58% top vs base
        height_initial = 0.15  # cm
        rise_angle = math.radians(90 - 6.666)   # ~83.334 deg from horizontal
        fall_angle = math.radians(90 - 23.3333) # ~66.6667 deg from horizontal

        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        lines = sketch.sketchCurves.sketchLines
        
        # Starting point (in cm)
        x, y = 0.0, 0.0
        prev_point = adsk.core.Point3D.create(x, y, 0)
        
        gap_size = 0.1  # The horizontal gap we want after each segment

        for i in range(num_sections):
            # Compute rise/fall/flat lengths
            factor = (rise_factor ** i)
            rise_length = height_initial * factor * cosec(rise_angle)
            fall_length = height_initial * factor * cosec(fall_angle)
            flat_length = flat_length_initial * factor

            # Rising segment
            x += rise_length * math.cos(rise_angle)
            y += rise_length * math.sin(rise_angle)
            rise_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, rise_point)
            prev_point = rise_point

            # Flat segment (horizontal)
            x += flat_length
            flat_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, flat_point)
            prev_point = flat_point

            # Falling segment
            x += fall_length * math.cos(fall_angle)
            y -= fall_length * math.sin(fall_angle)
            fall_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, fall_point)
            prev_point = fall_point

            # AFTER finishing this segment, jump x by 0.1 with NO line
            x += gap_size
            prev_point = adsk.core.Point3D.create(x, y, 0)

        # Optionally, you can comment this out if you don't want the elastic axis line
        join_radius = 0
        elastic_start = adsk.core.Point3D.create(0.0, join_radius, 0)
        elastic_end = adsk.core.Point3D.create(x, join_radius, 0)
        lines.addByTwoPoints(elastic_start, elastic_end)
        
        ui.messageBox('Profile created with a 0.1 cm gap after each segment.')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
