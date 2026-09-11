# Jetson-branded infinity cube (Ender-3 V2 G-code)

Post-processed from the original Cura slice `CE3E3V2_infinity_cube.gcode` (8 × 20 mm print-in-place cubes, 0.2 mm layers, single colour).
The Jetson wordmark is engraved 0.4 mm deep into one hinge-free face of every cube.

| File | What it is |
|---|---|
| `CE3E3V2_infinity_cube_jetson_horizontal.gcode` | Wordmark reads left-to-right on the side faces |
| `CE3E3V2_infinity_cube_jetson_vertical.gcode` | Wordmark rotated 90° (reads bottom-to-top) on the side faces; better letterforms |
| `CE3E3V2_infinity_cube_jetson_allfaces.gcode` | **Checkerboard of wordmarks and lightning bolts on all four side faces + top of every cube (40 faces)** |
| `build_all.py` | Generator for the all-faces file (surveys every face, picks per-face orientation) |
| `survey.py` | Stand-alone face survey: largest hinge-free rectangle on each vertical face |
| `verify_all.py` | Verification and elevation renders for the all-faces file |
| `build_gcode.py` | Generator. Edit `SRC` to point at the original G-code, run `python3 build_gcode.py` |
| `logo_geom.py` | Traces the brand-kit wordmark PNG into vector geometry |
| `verify.py` | Re-parses the output, checks extrusion continuity, renders the modified layers |

## Where the logo goes and why

* **Outer four cubes** (ends of the layout): the outward-facing long side is a clean 13.8 × 13.6 mm flat with no hinge.
  The wordmark is cut into it by removing the outer-wall bead where the letters fall; the inner wall becomes the recess floor.
  Side faces are built from 0.2 mm layers, so the letters are stair-stepped in Z.
* **Middle four cubes**: their long sides carry the hinge clearance slots (only 9.7 mm clear at mid height), so the wordmark
  is cut into the top face instead. The top two skin layers are regenerated with the letters as holes, with a perimeter bead
  around each letter for crisp edges. These faces get the true continuous outline.

Wordmark size: 13.4 mm on side faces, 11.8 mm on top faces. Strokes are widened by 0.08 mm and every cavity is forced to
at least 0.5 mm so a 0.4 mm nozzle can resolve it.

Dependencies for the scripts: `shapely`, `scikit-image`, `pillow`, `matplotlib`.

## All-faces version

`build_all.py` surveys all 32 vertical faces from the outer-wall paths and finds the largest flat, hinge-free
rectangle on each (13.8 × 14 mm on most, 13.8 × 10 where a hinge knuckle sits above or below, 9.7 × 14 on the
middle cubes' slotted long sides). Cubes alternate in a checkerboard: wordmark on (0,0), (2,0), (1,1), (3,1);
bolt on the rest. Each face gets the largest design that fits, the wordmark choosing horizontal, vertical or
diagonal (15.3 mm on the big faces). Top faces are clipped the same way; bottoms are untouched.
