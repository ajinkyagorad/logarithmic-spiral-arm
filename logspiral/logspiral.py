# Author-
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        
        # Parameters for the logarithmic spiral
        a = 1.78315  # Initial radius
        b = 0.15  # Growth rate
        num_points = 24+12+1  # Number of segments
        angle_step = math.radians(30)  # Ensure points align at 30-degree increments
        thickness = 2  # Thickness of the spiral extrusion
        #height_increment = 0.2  # Height difference between consecutive points
        
        # Create a new sketch
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = adsk.core.ObjectCollection.create()
        
        for i in range(num_points):
            theta = i * angle_step
            r = a * math.exp(b * theta)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.add(adsk.core.Point3D.create(x, y, 0))
        
        # Create a 2D spline
        spline = sketch.sketchCurves.sketchFittedSplines.add(points)
        
        # Add intersection points along theta = 30 degrees
        intersect_points = adsk.core.ObjectCollection.create()
        for i in range(1, num_points):
            if i % int(math.pi / angle_step) == 0:
                intersect_points.add(points.item(i))
        
        for point in intersect_points:
            sketch.sketchPoints.add(point)
        
        # Extrude the spiral curve
        profs = sketch.profiles
        if len(profs) > 0:
            extrudes = rootComp.features.extrudeFeatures
            extrudeInput = extrudes.createInput(profs.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distance = adsk.core.ValueInput.createByReal(thickness)
            extrudeInput.setDistanceExtent(False, distance)
            extrudes.add(extrudeInput)
        
        ui.messageBox('Logarithmic spiral 3D model created with intersection points at 30-degree intervals!')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
