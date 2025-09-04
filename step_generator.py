#!/usr/bin/env python3
"""
STEP File Generator for Geometric Entities
Preserves b1 point/line coordinates and generates surfaces and solids.
"""

import math
from typing import List, Tuple, Dict, Any
from datetime import datetime


class Point3D:
    """Represents a 3D point with x, y, z coordinates."""
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"Point3D({self.x}, {self.y}, {self.z})"


class Line3D:
    """Represents a 3D line defined by two points."""
    
    def __init__(self, start_point: Point3D, end_point: Point3D):
        self.start = start_point
        self.end = end_point
    
    def length(self) -> float:
        """Calculate the length of the line."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        dz = self.end.z - self.start.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def __str__(self):
        return f"Line3D({self.start}, {self.end})"


class B1Entity:
    """Container for b1 geometric entity with points and lines."""
    
    def __init__(self):
        self.points: List[Point3D] = []
        self.lines: List[Line3D] = []
        self.name = "B1"
    
    def add_point(self, point: Point3D):
        """Add a point to the b1 entity."""
        self.points.append(point)
    
    def add_line(self, line: Line3D):
        """Add a line to the b1 entity."""
        self.lines.append(line)
    
    def get_bounding_box(self) -> Tuple[Point3D, Point3D]:
        """Get the bounding box of all points."""
        if not self.points:
            return Point3D(0, 0, 0), Point3D(0, 0, 0)
        
        min_x = min(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        min_z = min(p.z for p in self.points)
        max_x = max(p.x for p in self.points)
        max_y = max(p.y for p in self.points)
        max_z = max(p.z for p in self.points)
        
        return Point3D(min_x, min_y, min_z), Point3D(max_x, max_y, max_z)


class STEPGenerator:
    """Generates STEP files from geometric entities."""
    
    def __init__(self):
        self.entity_counter = 1
        self.entities = []
    
    def _next_id(self) -> int:
        """Get the next entity ID."""
        current = self.entity_counter
        self.entity_counter += 1
        return current
    
    def _add_entity(self, entity_type: str, attributes: str) -> int:
        """Add an entity to the STEP file."""
        entity_id = self._next_id()
        self.entities.append(f"#{entity_id} = {entity_type}({attributes});")
        return entity_id
    
    def _cartesian_point(self, point: Point3D) -> int:
        """Create a CARTESIAN_POINT entity."""
        coords = f"({point.x},{point.y},{point.z})"
        return self._add_entity("CARTESIAN_POINT", f"'',{coords}")
    
    def _direction(self, dx: float, dy: float, dz: float) -> int:
        """Create a DIRECTION entity."""
        return self._add_entity("DIRECTION", f"'',({dx},{dy},{dz})")
    
    def _vector(self, direction_id: int, magnitude: float) -> int:
        """Create a VECTOR entity."""
        return self._add_entity("VECTOR", f"'',#{direction_id},{magnitude}")
    
    def _line(self, start_point_id: int, vector_id: int) -> int:
        """Create a LINE entity."""
        return self._add_entity("LINE", f"'',#{start_point_id},#{vector_id}")
    
    def _generate_surfaces_from_lines(self, b1: B1Entity) -> List[int]:
        """Generate surfaces from the lines in b1 entity."""
        surface_ids = []
        
        if len(b1.lines) >= 3:
            # Create a simple planar surface from the first 3 lines
            # This is a simplified approach - in practice, surface generation is more complex
            
            # Create points for the lines
            point_ids = []
            for line in b1.lines[:4]:  # Use first 4 lines to create a quadrilateral
                start_id = self._cartesian_point(line.start)
                end_id = self._cartesian_point(line.end)
                point_ids.extend([start_id, end_id])
            
            # Create a simple rectangular surface
            if len(point_ids) >= 4:
                # Create a PLANE entity
                origin_id = point_ids[0]
                normal_dir_id = self._direction(0, 0, 1)  # Z-direction normal
                plane_id = self._add_entity("PLANE", f"'',#{origin_id},#{normal_dir_id}")
                surface_ids.append(plane_id)
        
        return surface_ids
    
    def _generate_solid_from_surfaces(self, surface_ids: List[int], b1: B1Entity) -> int:
        """Generate a solid from surfaces."""
        if not surface_ids:
            return None
        
        # Create a simple box solid based on bounding box
        min_pt, max_pt = b1.get_bounding_box()
        
        # Create corner points of the box
        corners = [
            Point3D(min_pt.x, min_pt.y, min_pt.z),
            Point3D(max_pt.x, min_pt.y, min_pt.z),
            Point3D(max_pt.x, max_pt.y, min_pt.z),
            Point3D(min_pt.x, max_pt.y, min_pt.z),
            Point3D(min_pt.x, min_pt.y, max_pt.z),
            Point3D(max_pt.x, min_pt.y, max_pt.z),
            Point3D(max_pt.x, max_pt.y, max_pt.z),
            Point3D(min_pt.x, max_pt.y, max_pt.z),
        ]
        
        corner_ids = [self._cartesian_point(pt) for pt in corners]
        
        # Create a simplified solid representation
        solid_id = self._add_entity("BLOCK", f"'',#{corner_ids[0]},{max_pt.x-min_pt.x},{max_pt.y-min_pt.y},{max_pt.z-min_pt.z}")
        
        return solid_id
    
    def generate_step_file(self, b1: B1Entity, filename: str):
        """Generate a complete STEP file from b1 entity."""
        
        # Reset for new generation
        self.entity_counter = 1
        self.entities = []
        
        # Generate geometric entities from b1
        point_ids = []
        line_ids = []
        
        # Process points
        for point in b1.points:
            point_id = self._cartesian_point(point)
            point_ids.append(point_id)
        
        # Process lines
        for line in b1.lines:
            start_id = self._cartesian_point(line.start)
            
            # Calculate direction and magnitude
            dx = line.end.x - line.start.x
            dy = line.end.y - line.start.y
            dz = line.end.z - line.start.z
            magnitude = line.length()
            
            if magnitude > 0:
                # Normalize direction
                dx, dy, dz = dx/magnitude, dy/magnitude, dz/magnitude
                
                direction_id = self._direction(dx, dy, dz)
                vector_id = self._vector(direction_id, magnitude)
                line_id = self._line(start_id, vector_id)
                line_ids.append(line_id)
        
        # Generate surfaces from lines
        surface_ids = self._generate_surfaces_from_lines(b1)
        
        # Generate solid from surfaces
        solid_id = self._generate_solid_from_surfaces(surface_ids, b1)
        
        # Write STEP file
        self._write_step_file(filename, b1)
    
    def _write_step_file(self, filename: str, b1: B1Entity):
        """Write the complete STEP file."""
        
        with open(filename, 'w') as f:
            # STEP file header
            f.write("ISO-10303-21;\n")
            f.write("HEADER;\n")
            f.write("FILE_DESCRIPTION(('Generated STEP file for B1 entity'),'2;1');\n")
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            f.write(f"FILE_NAME('{filename}','{timestamp}',('STEP Generator'),('Python Script'),'','','');\n")
            f.write("FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));\n")
            f.write("ENDSEC;\n\n")
            
            # Data section
            f.write("DATA;\n")
            
            # Write all entities
            for entity in self.entities:
                f.write(entity + "\n")
            
            f.write("ENDSEC;\n")
            f.write("END-ISO-10303-21;\n")


def create_sample_b1_entity() -> B1Entity:
    """Create a sample b1 entity with points and lines for testing."""
    b1 = B1Entity()
    
    # Add sample points
    b1.add_point(Point3D(0, 0, 0))
    b1.add_point(Point3D(10, 0, 0))
    b1.add_point(Point3D(10, 10, 0))
    b1.add_point(Point3D(0, 10, 0))
    b1.add_point(Point3D(0, 0, 10))
    b1.add_point(Point3D(10, 0, 10))
    b1.add_point(Point3D(10, 10, 10))
    b1.add_point(Point3D(0, 10, 10))
    
    # Add sample lines connecting the points
    b1.add_line(Line3D(Point3D(0, 0, 0), Point3D(10, 0, 0)))
    b1.add_line(Line3D(Point3D(10, 0, 0), Point3D(10, 10, 0)))
    b1.add_line(Line3D(Point3D(10, 10, 0), Point3D(0, 10, 0)))
    b1.add_line(Line3D(Point3D(0, 10, 0), Point3D(0, 0, 0)))
    b1.add_line(Line3D(Point3D(0, 0, 0), Point3D(0, 0, 10)))
    b1.add_line(Line3D(Point3D(10, 0, 0), Point3D(10, 0, 10)))
    
    return b1


def main():
    """Main function to demonstrate STEP file generation."""
    print("STEP File Generator for B1 Entity")
    print("=" * 40)
    
    # Create sample b1 entity
    b1 = create_sample_b1_entity()
    
    print(f"B1 Entity: {b1.name}")
    print(f"Points: {len(b1.points)}")
    print(f"Lines: {len(b1.lines)}")
    
    # Display points and lines
    print("\nPoints in B1:")
    for i, point in enumerate(b1.points):
        print(f"  {i+1}: {point}")
    
    print("\nLines in B1:")
    for i, line in enumerate(b1.lines):
        print(f"  {i+1}: {line} (length: {line.length():.2f})")
    
    # Generate STEP file
    generator = STEPGenerator()
    output_filename = "b1_entity_output.step"
    
    print(f"\nGenerating STEP file: {output_filename}")
    generator.generate_step_file(b1, output_filename)
    
    print(f"STEP file generated successfully!")
    print(f"Output file: {output_filename}")
    
    # Display bounding box
    min_pt, max_pt = b1.get_bounding_box()
    print(f"\nBounding box:")
    print(f"  Min: {min_pt}")
    print(f"  Max: {max_pt}")


if __name__ == "__main__":
    main()