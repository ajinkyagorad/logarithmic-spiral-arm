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
        a = 1  # Initial radius
        b = 0.15  # Growth rate
        num_points = 24+12+1   # Number of segments
        angle_step = math.radians(30)  # Ensure points align at 30-degree increments
        thickness = 2  # Thickness of the spiral extrusion
        
        # Additional spiral parameters (starting from midpoint)
        a_prime = 1.78315  # New initial radius based on midpoint segment
        
        # Create a new sketch
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = adsk.core.ObjectCollection.create()
        middle_points = adsk.core.ObjectCollection.create()
        new_spiral_points = adsk.core.ObjectCollection.create()
        
        for i in range(num_points):
            theta = i * angle_step
            r = a * math.exp(b * theta)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.add(adsk.core.Point3D.create(x, y, 0))

            # Additional spiral starting from midpoint segment
            r_prime = a_prime * math.exp(b * theta)
            x_prime = r_prime * math.cos(theta)
            y_prime = r_prime * math.sin(theta)
            middle_points.add(adsk.core.Point3D.create(x_prime, y_prime, 0))
        
        # Create 2D splines for main, middle, and additional spiral
        #spline_main = sketch.sketchCurves.sketchFittedSplines.add(points)
        #spline_middle = sketch.sketchCurves.sketchFittedSplines.add(middle_points)
        
        # Connect points within each spiral
        for i in range(num_points - 1):
            sketch.sketchCurves.sketchLines.addByTwoPoints(points.item(i), points.item(i + 1))
            sketch.sketchCurves.sketchLines.addByTwoPoints(middle_points.item(i), middle_points.item(i + 1))
        
        # Join points between s_0 and s_mid along angles
        for i in range(num_points):
            sketch.sketchCurves.sketchLines.addByTwoPoints(points.item(i), middle_points.item(i))
            

            

        # from middle_points
        #             lines : 7.832 at angle 13.3333, (+30 deg for each next) #         # initial angle : 96.7  i.e  96.7 (angle of line w.r.t. x) -90+6.66666
        #             lines : 8.472 at angle -16.6666 (+30 deg for each next) #(angle of line w.r.t. x)
        # Create offset angled lines at 13.3333 and -16.6666 degrees clockwise
        base_angle = math.radians(0)  # Initial reference angle
        offset_angle_1 = math.radians(13.3333)  # First offset angle
        offset_angle_2 = math.radians(-16.6666)  # Second offset angle
        
        for i in range(num_points - 12):
            p1 = middle_points.item(i)
            p2 = points.item(i + 12)
            
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            base_length1 = .1* 7.832  # Base length for first offset line
            base_length2 = .1 * 8.472  # Base length for second offset line
            
            # Scale lengths according to the spiral growth
            growth_factor = math.exp(b * (i * angle_step))
            length1 = base_length1 * growth_factor
            growth_factor = math.exp(b * ((i-1) * angle_step))
            length2 = base_length2 * growth_factor

            x_offset1 = p1.x + length1 * math.cos(base_angle + offset_angle_1 + i * angle_step)
            y_offset1 = p1.y + length1 * math.sin(base_angle + offset_angle_1 + i * angle_step)
            x_offset2 = p1.x + length2 * math.cos(base_angle + offset_angle_2 + (i-1) * angle_step)
            y_offset2 = p1.y + length2 * math.sin(base_angle + offset_angle_2 + (i-1) * angle_step)
            

            offset_point1 = adsk.core.Point3D.create(x_offset1, y_offset1, 0)
            offset_point2 = adsk.core.Point3D.create(x_offset2, y_offset2, 0)
            
            sketch.sketchCurves.sketchLines.addByTwoPoints(p1, offset_point1)
            sketch.sketchCurves.sketchLines.addByTwoPoints(p1, offset_point2)
        
        ui.messageBox('Logarithmic spiral 3D model created with structured connections and offset angled lines!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
