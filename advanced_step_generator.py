#!/usr/bin/env python3
"""
Advanced STEP File Generator with B1 coordinate loading
Supports loading b1 coordinates from external files and advanced surface generation.
"""

import json
import sys
from step_generator import B1Entity, Point3D, Line3D, STEPGenerator


class B1Loader:
    """Loads B1 entity coordinates from various file formats."""
    
    @staticmethod
    def from_json(filename: str) -> B1Entity:
        """Load B1 entity from JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            b1 = B1Entity()
            
            # Load points
            if 'points' in data:
                for point_data in data['points']:
                    point = Point3D(point_data['x'], point_data['y'], point_data['z'])
                    b1.add_point(point)
            
            # Load lines
            if 'lines' in data:
                for line_data in data['lines']:
                    start = Point3D(line_data['start']['x'], line_data['start']['y'], line_data['start']['z'])
                    end = Point3D(line_data['end']['x'], line_data['end']['y'], line_data['end']['z'])
                    line = Line3D(start, end)
                    b1.add_line(line)
            
            return b1
            
        except Exception as e:
            print(f"Error loading B1 from JSON: {e}")
            return None
    
    @staticmethod
    def from_csv(filename: str) -> B1Entity:
        """Load B1 entity from CSV file."""
        try:
            b1 = B1Entity()
            
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.upper() == 'POINTS':
                    current_section = 'points'
                    continue
                elif line.upper() == 'LINES':
                    current_section = 'lines'
                    continue
                
                if current_section == 'points':
                    parts = line.split(',')
                    if len(parts) >= 3:
                        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                        b1.add_point(Point3D(x, y, z))
                
                elif current_section == 'lines':
                    parts = line.split(',')
                    if len(parts) >= 6:
                        x1, y1, z1 = float(parts[0]), float(parts[1]), float(parts[2])
                        x2, y2, z2 = float(parts[3]), float(parts[4]), float(parts[5])
                        start = Point3D(x1, y1, z1)
                        end = Point3D(x2, y2, z2)
                        b1.add_line(Line3D(start, end))
            
            return b1
            
        except Exception as e:
            print(f"Error loading B1 from CSV: {e}")
            return None


def create_sample_b1_json():
    """Create a sample B1 JSON file for testing."""
    sample_data = {
        "name": "B1_Sample",
        "points": [
            {"x": 0, "y": 0, "z": 0},
            {"x": 10, "y": 0, "z": 0},
            {"x": 10, "y": 10, "z": 0},
            {"x": 0, "y": 10, "z": 0},
            {"x": 0, "y": 0, "z": 10},
            {"x": 10, "y": 0, "z": 10},
            {"x": 10, "y": 10, "z": 10},
            {"x": 0, "y": 10, "z": 10}
        ],
        "lines": [
            {"start": {"x": 0, "y": 0, "z": 0}, "end": {"x": 10, "y": 0, "z": 0}},
            {"start": {"x": 10, "y": 0, "z": 0}, "end": {"x": 10, "y": 10, "z": 0}},
            {"start": {"x": 10, "y": 10, "z": 0}, "end": {"x": 0, "y": 10, "z": 0}},
            {"start": {"x": 0, "y": 10, "z": 0}, "end": {"x": 0, "y": 0, "z": 0}},
            {"start": {"x": 0, "y": 0, "z": 0}, "end": {"x": 0, "y": 0, "z": 10}},
            {"start": {"x": 10, "y": 0, "z": 0}, "end": {"x": 10, "y": 0, "z": 10}},
            {"start": {"x": 10, "y": 10, "z": 0}, "end": {"x": 10, "y": 10, "z": 10}},
            {"start": {"x": 0, "y": 10, "z": 0}, "end": {"x": 0, "y": 10, "z": 10}},
            {"start": {"x": 0, "y": 0, "z": 10}, "end": {"x": 10, "y": 0, "z": 10}},
            {"start": {"x": 10, "y": 0, "z": 10}, "end": {"x": 10, "y": 10, "z": 10}},
            {"start": {"x": 10, "y": 10, "z": 10}, "end": {"x": 0, "y": 10, "z": 10}},
            {"start": {"x": 0, "y": 10, "z": 10}, "end": {"x": 0, "y": 0, "z": 10}}
        ]
    }
    
    with open('b1_sample.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("Created sample B1 JSON file: b1_sample.json")


def create_sample_b1_csv():
    """Create a sample B1 CSV file for testing."""
    csv_content = """# B1 Entity Coordinate File
# Lines starting with # are comments
POINTS
# x,y,z coordinates
0,0,0
10,0,0
10,10,0
0,10,0
0,0,10
10,0,10
10,10,10
0,10,10
LINES
# x1,y1,z1,x2,y2,z2 (start and end coordinates)
0,0,0,10,0,0
10,0,0,10,10,0
10,10,0,0,10,0
0,10,0,0,0,0
0,0,0,0,0,10
10,0,0,10,0,10
10,10,0,10,10,10
0,10,0,0,10,10
0,0,10,10,0,10
10,0,10,10,10,10
10,10,10,0,10,10
0,10,10,0,0,10
"""
    
    with open('b1_sample.csv', 'w') as f:
        f.write(csv_content)
    
    print("Created sample B1 CSV file: b1_sample.csv")


def main():
    """Main function with command line interface."""
    print("Advanced STEP File Generator for B1 Entity")
    print("=" * 45)
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
        # Determine file type and load accordingly
        if input_file.endswith('.json'):
            print(f"Loading B1 entity from JSON file: {input_file}")
            b1 = B1Loader.from_json(input_file)
        elif input_file.endswith('.csv'):
            print(f"Loading B1 entity from CSV file: {input_file}")
            b1 = B1Loader.from_csv(input_file)
        else:
            print(f"Unsupported file format: {input_file}")
            print("Supported formats: .json, .csv")
            return
        
        if b1 is None:
            print("Failed to load B1 entity from file.")
            return
    else:
        print("No input file specified. Creating sample files and using default B1 entity.")
        
        # Create sample files
        create_sample_b1_json()
        create_sample_b1_csv()
        
        # Load from JSON sample
        b1 = B1Loader.from_json('b1_sample.json')
        if b1 is None:
            print("Failed to load sample B1 entity.")
            return
    
    print(f"\nLoaded B1 Entity: {b1.name}")
    print(f"Points: {len(b1.points)}")
    print(f"Lines: {len(b1.lines)}")
    
    # Display coordinate summary
    if b1.points:
        min_pt, max_pt = b1.get_bounding_box()
        print(f"\nCoordinate range:")
        print(f"  X: {min_pt.x} to {max_pt.x}")
        print(f"  Y: {min_pt.y} to {max_pt.y}")
        print(f"  Z: {min_pt.z} to {max_pt.z}")
    
    # Generate STEP file
    generator = STEPGenerator()
    output_filename = "b1_entity_advanced.step"
    
    print(f"\nGenerating STEP file: {output_filename}")
    generator.generate_step_file(b1, output_filename)
    
    print(f"STEP file generated successfully!")
    print(f"Output file: {output_filename}")
    
    # Display detailed information
    print(f"\nDetailed B1 Information:")
    print(f"  Total line length: {sum(line.length() for line in b1.lines):.2f}")
    if b1.lines:
        avg_length = sum(line.length() for line in b1.lines) / len(b1.lines)
        print(f"  Average line length: {avg_length:.2f}")


if __name__ == "__main__":
    main()