# Logarithmic Spiral Arm Generation
Based on the idea presented in Wang, Zhanchi, Nikolaos M. Freris, and Xi Wei. "SpiRobs: Logarithmic spiral-shaped robots for versatile grasping across scales." Device (2024).
This repository contains a Fusion 360 scripts for generating a profile for aiding in design of logarithmic spiral arm profile based on specified parameters in the script.

## Usage
1. Run the provided Fusion 360 script to generate the initial logarithmic spiral arm profile.
2. After running the script, **manual adjustments** to complete the design. 
3. The final design can be exported as an STL file for 3D printing or further modifications.
4. Fusion360 f3d file is provided.

Note. project is based on the given diagram, and does not articulately describe the entire arm, precise geometry and string could be necessary for desired performance, I have no idea as I myself haven't tried it yet.

## Embedded STL
For convenience, a pre-generated **cylindrical spiral arm** STL STEP  file is included in the repository:

![Logarithmic Spiral Arm](cylindrical_spiral_arm.stl)

## Notes
- Ensure that units are set to **millimeters (mm)** in Fusion 360 before running the script.
- Manual modifications might be needed for alignment and structural optimizations.
- attempted to make joined version of segments, it could be better to use loosesegments, and strong thread.
- Force required on string is limited to 60 N in the article by Wang et al.
- Arm can be extended just by printing a scaled version of it and attaching next to it, while taking care of holes for strings.
- Further, design of only single repeating scaled unit is required and in CAD, arm of any length can be made by scaling appropriately the repeating units.
- Currently arm joints are linked, with idea to avoid load on strings, but separately printed segments will not.

