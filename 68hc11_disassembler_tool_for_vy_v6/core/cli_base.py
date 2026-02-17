#!/usr/bin/env python3
"""
CLI Base Class - Standard command-line interface for all VY V6 tools
Provides consistent argument parsing, logging, and output management

Author: KingAI Automotive Research
Date: January 19, 2026
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json


class CLIBase:
    """Base class for all command-line tools"""
    
    # Tool metadata (override in subclass)
    TOOL_NAME = "Generic Tool"
    TOOL_DESCRIPTION = "Tool description"
    TOOL_VERSION = "1.0.0"
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=f"{self.TOOL_NAME} - {self.TOOL_DESCRIPTION}",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.args = None
        self.logger = None
        self.start_time = None
        self.setup_common_arguments()
        
    def setup_common_arguments(self):
        """Add standard arguments all tools should have"""
        # Input/Output
        self.parser.add_argument('--input', '-i', type=str,
                                help='Input file or directory')
        self.parser.add_argument('--output', '-o', type=str,
                                help='Output file or directory')
        self.parser.add_argument('--output-dir', type=str,
                                help='Output directory (auto-creates)')
        
        # Timestamps and naming
        self.parser.add_argument('--timestamp', action='store_true',
                                help='Add timestamp to output filenames')
        self.parser.add_argument('--prefix', type=str,
                                help='Prefix for output filenames')
        
        # Format options
        self.parser.add_argument('--format', choices=['txt', 'json', 'csv', 'md'],
                                default='txt', help='Output format')
        
        # Behavior options
        self.parser.add_argument('--dry-run', action='store_true',
                                help='Show what would be done without doing it')
        self.parser.add_argument('--force', action='store_true',
                                help='Overwrite existing files')
        self.parser.add_argument('--verbose', '-v', action='count', default=0,
                                help='Increase verbosity (-v, -vv, -vvv)')
        self.parser.add_argument('--quiet', '-q', action='store_true',
                                help='Suppress all output except errors')
        
        # Logging
        self.parser.add_argument('--log-file', type=str,
                                help='Write log to file')
        self.parser.add_argument('--no-log', action='store_true',
                                help='Disable logging')
        
        # Version
        self.parser.add_argument('--version', action='version',
                                version=f'{self.TOOL_NAME} {self.TOOL_VERSION}')
    
    def setup_logging(self):
        """Configure logging based on arguments"""
        if self.args.no_log:
            logging.disable(logging.CRITICAL)
            return
        
        # Determine log level
        if self.args.quiet:
            level = logging.ERROR
        elif self.args.verbose == 0:
            level = logging.INFO
        elif self.args.verbose == 1:
            level = logging.DEBUG
        else:  # -vv or more
            level = logging.DEBUG
        
        # Configure logger
        handlers = []
        
        # Console handler
        if not self.args.quiet:
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(level)
            console.setFormatter(logging.Formatter(
                '%(levelname)s: %(message)s'
            ))
            handlers.append(console)
        
        # File handler
        if self.args.log_file:
            log_path = Path(self.args.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            handlers.append(file_handler)
        
        logging.basicConfig(
            level=level,
            handlers=handlers,
            force=True
        )
        
        self.logger = logging.getLogger(self.TOOL_NAME)
    
    def get_output_path(self, base_name: str, extension: str = 'txt') -> Path:
        """Generate output path with timestamp and prefix"""
        if self.args.output:
            return Path(self.args.output)
        
        # Build filename
        parts = []
        if self.args.prefix:
            parts.append(self.args.prefix)
        parts.append(base_name)
        if self.args.timestamp:
            parts.append(datetime.now().strftime('%Y%m%d_%H%M%S'))
        
        filename = '_'.join(parts) + '.' + extension
        
        # Determine directory
        if self.args.output_dir:
            output_dir = Path(self.args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir / filename
        
        return Path(filename)
    
    def write_output(self, data: Any, output_path: Optional[Path] = None):
        """Write output in requested format"""
        if output_path is None:
            output_path = self.get_output_path('output', self.args.format)
        
        if self.args.dry_run:
            self.logger.info(f"[DRY RUN] Would write to: {output_path}")
            return
        
        if output_path.exists() and not self.args.force:
            self.logger.error(f"Output file exists: {output_path} (use --force)")
            sys.exit(1)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.args.format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif self.args.format == 'csv':
            import csv
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                if isinstance(data, dict):
                    writer = csv.DictWriter(f, fieldnames=data.keys())
                    writer.writeheader()
                    writer.writerow(data)
                elif isinstance(data, list) and len(data) > 0:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        else:  # txt or md
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(data))
        
        self.logger.info(f"✅ Output written to: {output_path}")
    
    def run(self):
        """Main entry point - override in subclass"""
        raise NotImplementedError("Subclass must implement run()")
    
    def execute(self):
        """Execute the tool with full lifecycle"""
        self.start_time = datetime.now()
        
        # Parse arguments
        self.args = self.parser.parse_args()
        
        # Setup logging
        self.setup_logging()
        
        # Log start
        self.logger.info("=" * 70)
        self.logger.info(f"{self.TOOL_NAME} v{self.TOOL_VERSION}")
        self.logger.info("=" * 70)
        
        try:
            # Run the tool
            result = self.run()
            
            # Log completion
            elapsed = datetime.now() - self.start_time
            self.logger.info("=" * 70)
            self.logger.info(f"✅ Completed in {elapsed.total_seconds():.2f}s")
            self.logger.info("=" * 70)
            
            return result
            
        except KeyboardInterrupt:
            self.logger.warning("\n⚠️  Interrupted by user")
            sys.exit(130)
        except Exception as e:
            self.logger.error(f"❌ Error: {e}", exc_info=self.args.verbose > 1)
            sys.exit(1)


def main():
    """Example usage"""
    class ExampleTool(CLIBase):
        TOOL_NAME = "Example Tool"
        TOOL_DESCRIPTION = "Example tool demonstrating CLI base class"
        TOOL_VERSION = "1.0.0"
        
        def run(self):
            self.logger.info("Tool is running!")
            self.logger.debug(f"Arguments: {self.args}")
            
            data = {
                "tool": self.TOOL_NAME,
                "timestamp": datetime.now().isoformat(),
                "args": vars(self.args)
            }
            
            self.write_output(data)
    
    tool = ExampleTool()
    tool.execute()


if __name__ == "__main__":
    main()
