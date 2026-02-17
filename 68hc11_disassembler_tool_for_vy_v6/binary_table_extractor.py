#!/usr/bin/env python3
"""
Binary Table Extractor - Extract Actual Table Data from ECU Binaries
Uses XDF definitions to extract real calibration data from binary files
Exports tables to CSV, JSON, or TunerPro-compatible formats

Features:
- Extract tables by address using XDF definitions
- Decode data types (uint8, uint16, int8, int16)
- Export to multiple formats (CSV, JSON, hex dump)
- Compare table data between Stock and Enhanced OS
- Validate XDF addresses against binary reality

Author: Jason King (KingAIAuto)
Date: November 19, 2025
Project: VY V6 $060A ECU Reverse Engineering
"""

import xml.etree.ElementTree as ET
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import struct
import csv
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BinaryTableExtractor:
    """Extract table data from ECU binary using XDF definitions"""
    
    def __init__(self, binary_path: Path, xdf_path: Path):
        self.binary_path = binary_path
        self.xdf_path = xdf_path
        self.binary_data = bytearray(binary_path.read_bytes())
        self.xdf_definitions: Dict[str, Dict] = {}
        
        logger.info(f"Loaded binary: {len(self.binary_data)} bytes")
    
    def parse_xdf(self) -> bool:
        """Parse XDF file and extract table definitions"""
        try:
            tree = ET.parse(self.xdf_path)
            root = tree.getroot()
            
            # Parse tables
            for table in root.findall('.//XDFTABLE'):
                title_elem = table.find('title')
                if title_elem is None or not title_elem.text:
                    continue
                
                title = title_elem.text.strip()
                
                # Get Z-axis (table data)
                z_axis = table.find('.//XDFAXIS[@id="z"]')
                if z_axis is None:
                    continue
                
                embedded = z_axis.find('EMBEDDEDDATA')
                if embedded is None:
                    continue
                
                address_str = embedded.get('mmedaddress')
                if not address_str:
                    continue
                
                rows = int(embedded.get('mmedrowcount', '1'))
                cols = int(embedded.get('mmedcolcount', '1'))
                type_flags = embedded.get('mmedtypeflags', '0x02')  # Default unsigned
                elem_size_bits = int(embedded.get('mmedelementsizebits', '8'))
                
                # Get units
                units_elem = z_axis.find('units')
                units = units_elem.text if units_elem is not None and units_elem.text else ''
                
                # Get axis information
                x_axis_info = self._parse_axis(table.find('.//XDFAXIS[@id="x"]'))
                y_axis_info = self._parse_axis(table.find('.//XDFAXIS[@id="y"]'))
                
                self.xdf_definitions[title] = {
                    'type': 'TABLE',
                    'address': int(address_str, 0),
                    'rows': rows,
                    'cols': cols,
                    'size': rows * cols * (elem_size_bits // 8),
                    'elem_size_bits': elem_size_bits,
                    'type_flags': int(type_flags, 0),
                    'units': units,
                    'x_axis': x_axis_info,
                    'y_axis': y_axis_info
                }
            
            logger.info(f"Parsed XDF: {len(self.xdf_definitions)} table definitions")
            return True
            
        except Exception as e:
            logger.error(f"Error parsing XDF: {e}")
            return False
    
    def _parse_axis(self, axis_elem) -> Optional[Dict]:
        """Parse X or Y axis information"""
        if axis_elem is None:
            return None
        
        embedded = axis_elem.find('EMBEDDEDDATA')
        if embedded is None:
            return None
        
        address_str = embedded.get('mmedaddress')
        index_count = embedded.get('indexcount')
        
        units_elem = axis_elem.find('units')
        units = units_elem.text if units_elem is not None and units_elem.text else ''
        
        label_elem = axis_elem.find('.//LABEL')
        label = label_elem.get('value') if label_elem is not None else ''
        
        return {
            'address': int(address_str, 0) if address_str else None,
            'count': int(index_count) if index_count else None,
            'units': units,
            'label': label
        }
    
    def extract_table(self, title: str) -> Optional[Dict]:
        """Extract a specific table by title"""
        if title not in self.xdf_definitions:
            logger.error(f"Table '{title}' not found in XDF")
            return None
        
        defn = self.xdf_definitions[title]
        address = defn['address']
        size = defn['size']
        
        # Validate address is within binary
        if address + size > len(self.binary_data):
            logger.error(f"Table '{title}' address 0x{address:X} + {size} exceeds binary size")
            return None
        
        # Extract raw bytes
        raw_data = self.binary_data[address:address + size]
        
        # Decode based on data type
        decoded_values = self._decode_values(
            raw_data, 
            defn['elem_size_bits'],
            defn['type_flags'],
            defn['rows'] * defn['cols']
        )
        
        # Reshape into 2D array
        table_data = []
        for row_idx in range(defn['rows']):
            row_start = row_idx * defn['cols']
            row_end = row_start + defn['cols']
            table_data.append(decoded_values[row_start:row_end])
        
        return {
            'title': title,
            'address': f"0x{address:X}",
            'rows': defn['rows'],
            'cols': defn['cols'],
            'units': defn['units'],
            'data': table_data,
            'raw_hex': raw_data.hex(),
            'x_axis': defn['x_axis'],
            'y_axis': defn['y_axis']
        }
    
    def _decode_values(self, raw_data: bytes, elem_size_bits: int, type_flags: int, count: int) -> List[Any]:
        """Decode raw bytes into values based on type flags"""
        values = []
        elem_size_bytes = elem_size_bits // 8
        
        is_signed = bool(type_flags & 0x01)
        is_little_endian = bool(type_flags & 0x04)
        endian = '<' if is_little_endian else '>'
        
        # Determine struct format
        if elem_size_bits == 8:
            fmt = 'b' if is_signed else 'B'
        elif elem_size_bits == 16:
            fmt = 'h' if is_signed else 'H'
        elif elem_size_bits == 32:
            fmt = 'i' if is_signed else 'I'
        else:
            logger.warning(f"Unsupported element size: {elem_size_bits} bits")
            return []
        
        # Unpack values
        for i in range(count):
            offset = i * elem_size_bytes
            if offset + elem_size_bytes <= len(raw_data):
                value = struct.unpack(f'{endian}{fmt}', raw_data[offset:offset + elem_size_bytes])[0]
                values.append(value)
        
        return values
    
    def extract_all_spark_tables(self) -> List[Dict]:
        """Extract all spark-related tables"""
        spark_keywords = ['SPARK', 'TIMING', 'ADVANCE', 'RETARD', 'IGNITION']
        spark_tables = []
        
        for title in self.xdf_definitions.keys():
            if any(keyword in title.upper() for keyword in spark_keywords):
                table = self.extract_table(title)
                if table:
                    spark_tables.append(table)
        
        logger.info(f"Extracted {len(spark_tables)} spark tables")
        return spark_tables
    
    def extract_all_fuel_tables(self) -> List[Dict]:
        """Extract all fuel-related tables"""
        fuel_keywords = ['FUEL', 'AFR', 'INJECTOR', 'PE ', 'POWER ENRICHMENT']
        fuel_tables = []
        
        for title in self.xdf_definitions.keys():
            if any(keyword in title.upper() for keyword in fuel_keywords):
                table = self.extract_table(title)
                if table:
                    fuel_tables.append(table)
        
        logger.info(f"Extracted {len(fuel_tables)} fuel tables")
        return fuel_tables
    
    def export_table_to_csv(self, table_data: Dict, output_path: Path):
        """Export a single table to CSV"""
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([f"Title: {table_data['title']}"])
                writer.writerow([f"Address: {table_data['address']}"])
                writer.writerow([f"Dimensions: {table_data['rows']}x{table_data['cols']}"])
                writer.writerow([f"Units: {table_data['units']}"])
                writer.writerow([])
                
                # Column headers (X-axis if available)
                if table_data.get('x_axis'):
                    writer.writerow([''] + [f"Col{i}" for i in range(table_data['cols'])])
                
                # Data rows
                for row_idx, row in enumerate(table_data['data']):
                    row_label = f"Row{row_idx}"
                    if table_data.get('y_axis'):
                        row_label = f"Y{row_idx}"
                    writer.writerow([row_label] + row)
            
            logger.info(f"✓ Exported: {output_path.name}")
            
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
    
    def export_table_to_json(self, table_data: Dict, output_path: Path):
        """Export a single table to JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(table_data, f, indent=2)
            
            logger.info(f"✓ Exported: {output_path.name}")
            
        except Exception as e:
            logger.error(f"Error exporting JSON: {e}")
    
    def compare_with_other_binary(self, other_extractor: 'BinaryTableExtractor', title: str) -> Optional[Dict]:
        """Compare a table between two binaries"""
        table1 = self.extract_table(title)
        table2 = other_extractor.extract_table(title)
        
        if not table1 or not table2:
            return None
        
        differences = []
        for row_idx in range(min(len(table1['data']), len(table2['data']))):
            for col_idx in range(min(len(table1['data'][row_idx]), len(table2['data'][row_idx]))):
                val1 = table1['data'][row_idx][col_idx]
                val2 = table2['data'][row_idx][col_idx]
                
                if val1 != val2:
                    differences.append({
                        'row': row_idx,
                        'col': col_idx,
                        'binary1_value': val1,
                        'binary2_value': val2,
                        'difference': val2 - val1
                    })
        
        return {
            'title': title,
            'total_cells': table1['rows'] * table1['cols'],
            'differences_count': len(differences),
            'differences': differences,
            'identical': len(differences) == 0
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Extract table data from ECU binary using XDF definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Extract a specific table
  python binary_table_extractor.py \\
    -b binary.bin -x definitions.xdf \\
    --table "Main Spark Advance Table" \\
    --csv output.csv

  # Extract all spark tables
  python binary_table_extractor.py \\
    -b binary.bin -x definitions.xdf \\
    --category spark --output-dir spark_tables/

  # Compare table between Stock and Enhanced
  python binary_table_extractor.py \\
    -b stock.bin -x stock.xdf \\
    -b2 enhanced.bin -x2 enhanced.xdf \\
    --table "Main Spark Advance Table" --compare
        '''
    )
    
    parser.add_argument(
        '-b', '--binary',
        type=Path,
        required=True,
        help='ECU binary file'
    )
    
    parser.add_argument(
        '-x', '--xdf',
        type=Path,
        required=True,
        help='XDF definition file'
    )
    
    parser.add_argument(
        '--table',
        help='Specific table title to extract'
    )
    
    parser.add_argument(
        '--category',
        choices=['spark', 'fuel', 'maf', 'all'],
        help='Extract all tables in category'
    )
    
    parser.add_argument(
        '--csv',
        type=Path,
        help='Export to CSV file'
    )
    
    parser.add_argument(
        '--json',
        type=Path,
        help='Export to JSON file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for batch export'
    )
    
    parser.add_argument(
        '-b2', '--binary2',
        type=Path,
        help='Second binary for comparison'
    )
    
    parser.add_argument(
        '-x2', '--xdf2',
        type=Path,
        help='Second XDF for comparison'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare table between two binaries'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validate files
    if not args.binary.exists():
        logger.error(f"Binary not found: {args.binary}")
        return 1
    
    if not args.xdf.exists():
        logger.error(f"XDF not found: {args.xdf}")
        return 1
    
    # Create extractor
    extractor = BinaryTableExtractor(args.binary, args.xdf)
    if not extractor.parse_xdf():
        return 1
    
    # Compare mode
    if args.compare:
        if not args.binary2 or not args.xdf2:
            logger.error("--compare requires --binary2 and --xdf2")
            return 1
        
        extractor2 = BinaryTableExtractor(args.binary2, args.xdf2)
        if not extractor2.parse_xdf():
            return 1
        
        if args.table:
            comparison = extractor.compare_with_other_binary(extractor2, args.table)
            if comparison:
                logger.info(f"\n{'='*80}")
                logger.info(f"TABLE COMPARISON: {comparison['title']}")
                logger.info(f"{'='*80}")
                logger.info(f"Total cells: {comparison['total_cells']}")
                logger.info(f"Differences: {comparison['differences_count']}")
                logger.info(f"Identical: {comparison['identical']}")
                
                if comparison['differences']:
                    logger.info(f"\nFirst 10 differences:")
                    for diff in comparison['differences'][:10]:
                        logger.info(f"  Row {diff['row']}, Col {diff['col']}: {diff['binary1_value']} → {diff['binary2_value']} (Δ{diff['difference']:+d})")
        
        return 0
    
    # Extract specific table
    if args.table:
        table_data = extractor.extract_table(args.table)
        if not table_data:
            return 1
        
        logger.info(f"\n✓ Extracted '{table_data['title']}'")
        logger.info(f"  Address: {table_data['address']}")
        logger.info(f"  Dimensions: {table_data['rows']}x{table_data['cols']}")
        logger.info(f"  Units: {table_data['units']}")
        
        # Export
        if args.csv:
            extractor.export_table_to_csv(table_data, args.csv)
        
        if args.json:
            extractor.export_table_to_json(table_data, args.json)
        
        return 0
    
    # Extract category
    if args.category:
        if args.category == 'spark':
            tables = extractor.extract_all_spark_tables()
        elif args.category == 'fuel':
            tables = extractor.extract_all_fuel_tables()
        else:
            tables = []
        
        if args.output_dir:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            
            for table in tables:
                safe_name = table['title'].replace('/', '_').replace('\\', '_').replace(' ', '_')
                csv_path = args.output_dir / f"{safe_name}.csv"
                extractor.export_table_to_csv(table, csv_path)
        
        return 0
    
    logger.error("Must specify --table or --category")
    return 1


if __name__ == '__main__':
    exit(main())
