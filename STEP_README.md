# STEP File Generator

This Python script generates STEP files from geometric entities, preserving b1 point and line coordinates and creating surfaces and solids according to STEP entity file requirements.

## Features

- Preserves b1 entity point and line geometric coordinates
- Generates surfaces from line entities
- Creates solid entities from surfaces
- Outputs standard STEP format files (ISO 10303-21)
- Supports 3D geometric primitives (points, lines, surfaces, solids)

## Usage

Run the script directly to generate a sample STEP file:

```bash
python3 step_generator.py
```

This will create a sample b1 entity with points and lines, then generate a STEP file called `b1_entity_output.step`.

## Output

The script generates a STEP file containing:
- Preserved original b1 point coordinates
- Line entities connecting the points
- Surface entities generated from the lines
- Solid entities created from the surfaces

## STEP File Format

The generated STEP files follow the ISO 10303-21 standard and include:
- File header with metadata
- Geometric entities (points, lines, surfaces, solids)
- Proper STEP entity relationships and references

## Example

Running the script creates a cube-like geometry with 8 points connected by lines, with generated surfaces and a solid entity.