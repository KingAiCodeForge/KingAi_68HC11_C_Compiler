#!/usr/bin/env python3
"""
Output Manager - Centralized output formatting and file management
Handles timestamped outputs, multiple formats, and organized directory structures

Author: Jason King
Date: January 19, 2026
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import logging


class OutputManager:
    """Manages all output operations with consistent formatting"""
    
    def __init__(self, 
                 base_dir: Union[str, Path] = ".",
                 timestamp: bool = True,
                 create_subdirs: bool = True):
        """
        Initialize output manager
        
        Args:
            base_dir: Base directory for all outputs
            timestamp: Add timestamps to filenames
            create_subdirs: Create subdirectories by category
        """
        self.base_dir = Path(base_dir)
        self.timestamp = timestamp
        self.create_subdirs = create_subdirs
        self.logger = logging.getLogger(__name__)
        
        # Create base directory
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.files_written = 0
        self.bytes_written = 0
    
    def get_timestamp(self) -> str:
        """Get formatted timestamp string"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def build_filename(self, 
                      base_name: str,
                      extension: str,
                      prefix: str = "",
                      suffix: str = "") -> str:
        """
        Build filename with optional timestamp
        
        Args:
            base_name: Base filename
            extension: File extension (without dot)
            prefix: Optional prefix
            suffix: Optional suffix
            
        Returns:
            Complete filename
        """
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(base_name)
        if suffix:
            parts.append(suffix)
        if self.timestamp:
            parts.append(self.get_timestamp())
        
        filename = '_'.join(parts) + '.' + extension
        return filename
    
    def get_output_path(self,
                       filename: str,
                       subdir: Optional[str] = None) -> Path:
        """
        Get full output path
        
        Args:
            filename: Filename to write
            subdir: Optional subdirectory
            
        Returns:
            Full path to output file
        """
        if self.create_subdirs and subdir:
            output_dir = self.base_dir / subdir
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir / filename
        return self.base_dir / filename
    
    def write_text(self,
                  content: str,
                  filename: str,
                  subdir: Optional[str] = None,
                  encoding: str = 'utf-8') -> Path:
        """
        Write text file
        
        Args:
            content: Text content
            filename: Output filename
            subdir: Optional subdirectory
            encoding: Text encoding
            
        Returns:
            Path to written file
        """
        output_path = self.get_output_path(filename, subdir)
        
        with open(output_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        self.files_written += 1
        self.bytes_written += output_path.stat().st_size
        self.logger.info(f"✅ Wrote text: {output_path}")
        
        return output_path
    
    def write_json(self,
                  data: Any,
                  filename: str,
                  subdir: Optional[str] = None,
                  indent: int = 2) -> Path:
        """
        Write JSON file
        
        Args:
            data: Data to serialize
            filename: Output filename
            subdir: Optional subdirectory
            indent: JSON indentation
            
        Returns:
            Path to written file
        """
        output_path = self.get_output_path(filename, subdir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        self.files_written += 1
        self.bytes_written += output_path.stat().st_size
        self.logger.info(f"✅ Wrote JSON: {output_path}")
        
        return output_path
    
    def write_csv(self,
                 data: List[Dict],
                 filename: str,
                 subdir: Optional[str] = None,
                 fieldnames: Optional[List[str]] = None) -> Path:
        """
        Write CSV file
        
        Args:
            data: List of dictionaries
            filename: Output filename
            subdir: Optional subdirectory
            fieldnames: Optional field order
            
        Returns:
            Path to written file
        """
        if not data:
            raise ValueError("No data to write")
        
        output_path = self.get_output_path(filename, subdir)
        
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        self.files_written += 1
        self.bytes_written += output_path.stat().st_size
        self.logger.info(f"✅ Wrote CSV: {output_path} ({len(data)} rows)")
        
        return output_path
    
    def write_markdown(self,
                      content: str,
                      filename: str,
                      subdir: Optional[str] = None,
                      title: Optional[str] = None,
                      metadata: Optional[Dict] = None) -> Path:
        """
        Write Markdown file with optional frontmatter
        
        Args:
            content: Markdown content
            filename: Output filename
            subdir: Optional subdirectory
            title: Optional document title
            metadata: Optional YAML frontmatter
            
        Returns:
            Path to written file
        """
        output_path = self.get_output_path(filename, subdir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Add frontmatter if provided
            if metadata or title:
                f.write("---\n")
                if title:
                    f.write(f"title: {title}\n")
                if metadata:
                    for key, value in metadata.items():
                        f.write(f"{key}: {value}\n")
                f.write(f"date: {datetime.now().isoformat()}\n")
                f.write("---\n\n")
            
            # Write content
            f.write(content)
        
        self.files_written += 1
        self.bytes_written += output_path.stat().st_size
        self.logger.info(f"✅ Wrote Markdown: {output_path}")
        
        return output_path
    
    def write_binary(self,
                    data: bytes,
                    filename: str,
                    subdir: Optional[str] = None) -> Path:
        """
        Write binary file
        
        Args:
            data: Binary data
            filename: Output filename
            subdir: Optional subdirectory
            
        Returns:
            Path to written file
        """
        output_path = self.get_output_path(filename, subdir)
        
        with open(output_path, 'wb') as f:
            f.write(data)
        
        self.files_written += 1
        self.bytes_written += len(data)
        self.logger.info(f"✅ Wrote binary: {output_path} ({len(data)} bytes)")
        
        return output_path
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get output statistics"""
        return {
            'files_written': self.files_written,
            'bytes_written': self.bytes_written,
            'mb_written': self.bytes_written / (1024 * 1024),
            'base_dir': str(self.base_dir.absolute())
        }
    
    def print_summary(self):
        """Print output summary"""
        stats = self.get_statistics()
        print(f"\n{'='*60}")
        print(f"Output Summary")
        print(f"{'='*60}")
        print(f"Files written: {stats['files_written']}")
        print(f"Total size: {stats['mb_written']:.2f} MB")
        print(f"Output directory: {stats['base_dir']}")
        print(f"{'='*60}\n")


def main():
    """Example usage"""
    logging.basicConfig(level=logging.INFO)
    
    # Create output manager
    manager = OutputManager(
        base_dir="output_test",
        timestamp=True,
        create_subdirs=True
    )
    
    # Write various formats
    manager.write_text("Hello, World!", "test.txt", subdir="text")
    
    manager.write_json({
        "tool": "example",
        "data": [1, 2, 3]
    }, "test.json", subdir="json")
    
    manager.write_csv([
        {"name": "Rev Limiter", "address": "0x77DE", "value": 236},
        {"name": "Fuel Map", "address": "0x6000", "value": 128}
    ], "test.csv", subdir="csv")
    
    manager.write_markdown(
        "# Test Document\n\nThis is a test.",
        "test.md",
        subdir="markdown",
        title="Test Markdown",
        metadata={"author": "KingAI", "version": "1.0"}
    )
    
    # Show summary
    manager.print_summary()


if __name__ == "__main__":
    main()
