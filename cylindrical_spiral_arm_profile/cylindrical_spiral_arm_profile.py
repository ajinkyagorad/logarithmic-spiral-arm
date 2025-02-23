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
        rise_factor = 1.05  # Progressive growth factor for rise
        flat_length_initial = 0.78*.15  # Flat section length in cm (58% top than base)
        height_initial = 0.15  # Initial height in cm (radius of smallest end)
        rise_angle = math.radians(90 - 6.666)  # Rising angle converted to radians
        fall_angle = math.radians(90 - 23.3333)  # Falling angle converted to radians
        
        # Create a new sketch
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        lines = sketch.sketchCurves.sketchLines
        
        # Starting point (in cm)
        x, y = 0.0, 0.0
        prev_point = adsk.core.Point3D.create(x, y, 0)
        
        points = []
        for i in range(num_sections):
            # Compute rise and fall distances progressively (in cm)
            rise_length = (height_initial * (rise_factor ** i) * cosec(rise_angle))
            fall_length = (height_initial * (rise_factor ** i) * cosec(fall_angle))
            flat_length = flat_length_initial * (rise_factor ** i)
            
            # Rising segment
            x += rise_length * math.cos(rise_angle)
            y += rise_length * math.sin(rise_angle)
            rise_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, rise_point)
            prev_point = rise_point
            points.append(rise_point)
            
            # Flat segment (horizontal)
            x += flat_length 
            flat_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, flat_point)
            prev_point = flat_point
            points.append(flat_point)
            
            # Falling segment
            x += fall_length * math.cos(fall_angle)
            y -= fall_length * math.sin(fall_angle)
            fall_point = adsk.core.Point3D.create(x, y, 0)
            lines.addByTwoPoints(prev_point, fall_point)
            prev_point = fall_point
            points.append(fall_point)
        
        # Connect the first and last points to close the profile
        #lines.addByTwoPoints(points[-1], points[0])
        
        # Elastic axis
        join_radius = 0
        elastic_start = adsk.core.Point3D.create(0.0, join_radius, 0)
        elastic_end = adsk.core.Point3D.create(x, join_radius, 0)
        lines.addByTwoPoints(elastic_start, elastic_end)
        
        # Revolve the profile around the elastic axis
        #prof = sketch.profiles.item(0)
        #revolve_features = rootComp.features.revolveFeatures
        #revolve_axis = lines[lines.count - 1]  # Get the last line (elastic axis)
        #revolve_input = revolve_features.createInput(prof, revolve_axis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        #revolve_angle = adsk.core.ValueInput.createByReal(math.radians(360))
        #revolve_input.setAngleExtent(False, revolve_angle)
        #revolve_features.add(revolve_input)
        
        ui.messageBox('Elastic axis profile revolved and generated with correct cm units!')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
