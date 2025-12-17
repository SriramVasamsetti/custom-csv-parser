# Custom CSV Parser

A comprehensive custom CSV parser implementation in Python that demonstrates fundamental concepts of data serialization and file I/O handling.

## Project Overview

This project develops a custom CSV (Comma-Separated Values) reader and writer in pure Python, without relying on Python's built-in csv module.

## Features

### CustomCsvReader
- Iterator-based design using __iter__ and __next__ methods
- Proper handling of quoted fields
- Support for escaped quotes ("" as single ")
- Support for multiline fields
- Streaming/memory-efficient processing

### CustomCsvWriter
- Automatic quoting of fields with commas, quotes, or newlines
- Proper escaping of internal quotes
- Row-by-row writing of list-of-lists
- RFC 4180 compliant output

## Installation & Setup

### Prerequisites
- Python 3.7 or higher

### Steps

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run benchmark: `python benchmark.py`

## Usage Examples

### Reading CSV Files

```python
from csv_parser import CustomCsvReader

with open('data.csv', 'r') as file:
    reader = CustomCsvReader(file)
    for row in reader:
        print(row)  # Each row is a list of strings
```

### Writing CSV Files

```python
from csv_parser import CustomCsvWriter

data = [
    ['Name', 'Age', 'City'],
    ['John Doe', '28', 'New York'],
    ['Jane Smith', '34', 'Los Angeles']
]

with open('output.csv', 'w') as file:
    writer = CustomCsvWriter(file)
    writer.writerows(data)
```

## Implementation Details

### CustomCsvReader Architecture
- State machine approach for parsing
- Character-by-character processing
- Tracks whether inside quoted fields
- Yields complete rows as lists of strings

### CustomCsvWriter Architecture
- Analyzes each field for quoting requirements
- Escapes quotes by doubling them
- Joins fields with commas
- Uses context managers for safe file handling

## Performance Benchmarking

Run `python benchmark.py` to benchmark against Python's standard csv library.

The benchmark includes:
- 10,000+ rows with 5 columns
- Comparison of read/write speeds
- Performance analysis and results

## Code Quality

- Adheres to PEP 8 style guidelines
- Uses context managers for all file operations
- Comprehensive docstrings for all classes and methods
- Proper error handling for edge cases
- Clear inline comments explaining complex logic

## Testing

Tested with:
- Standard CSV files
- Quoted fields with commas and quotes
- Embedded newlines
- Escape sequences
- Edge cases and special characters
- Large files (10,000+ rows)

## Learning Outcomes

1. File I/O and string manipulation
2. State machine design for parsing
3. Iterator protocol implementation
4. Performance analysis and benchmarking
5. Data serialization concepts
6. Professional Python coding standards

## References

- RFC 4180: CSV Format Specification
- Python CSV Module Documentation
- PEP 8 Style Guide

## Author

Sriram Vasamsetti

## License

MIT License
