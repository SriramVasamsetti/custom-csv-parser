"""Performance benchmarking for custom CSV parser.

This script compares the performance of the custom CSV parser
against Python's built-in csv module.
"""

import csv
import timeit
import random
import string
from io import StringIO
from csv_parser import CustomCsvReader, CustomCsvWriter


def generate_test_data(rows=10000, cols=5):
    """Generate synthetic CSV test data.
    
    Args:
        rows: Number of rows to generate
        cols: Number of columns per row
        
    Returns:
        List of lists containing test data
    """
    data = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            # Generate random field data with varying complexity
            field_type = random.choice(['simple', 'quoted', 'multiline'])
            if field_type == 'simple':
                field = ''.join(random.choices(string.ascii_letters, k=10))
            elif field_type == 'quoted':
                field = ''.join(random.choices(string.ascii_letters, k=10)) + ',quoted'
            else:  # multiline
                field = 'Line 1\nLine 2'
            row.append(field)
        data.append(row)
    return data


def benchmark_write(data, writer_class, iterations=5):
    """Benchmark writing CSV data.
    
    Args:
        data: Test data to write
        writer_class: CSV writer class to benchmark
        iterations: Number of times to run the benchmark
        
    Returns:
        Average time in seconds
    """
    times = []
    for _ in range(iterations):
        output = StringIO()
        start = timeit.default_timer()
        
        writer = writer_class(output)
        writer.writerows(data)
        
        end = timeit.default_timer()
        times.append(end - start)
    
    return sum(times) / len(times)


def benchmark_read(csv_text, reader_class, iterations=5):
    """Benchmark reading CSV data.
    
    Args:
        csv_text: CSV text to read
        reader_class: CSV reader class to benchmark
        iterations: Number of times to run the benchmark
        
    Returns:
        Average time in seconds
    """
    times = []
    for _ in range(iterations):
        start = timeit.default_timer()
        
        file_obj = StringIO(csv_text)
        reader = reader_class(file_obj)
        rows = list(reader)
        
        end = timeit.default_timer()
        times.append(end - start)
    
    return sum(times) / len(times)


def main():
    """Run the benchmark comparison."""
    print("\n" + "="*60)
    print("CSV Parser Performance Benchmark")
    print("="*60)
    
    # Generate test data
    print("\nGenerating test data...")
    test_data = generate_test_data(rows=10000, cols=5)
    print(f"Generated {len(test_data)} rows x 5 columns")
    
    # Write test data using custom writer
    print("\nWriting test data with CustomCsvWriter...")
    output = StringIO()
    writer = CustomCsvWriter(output)
    writer.writerows(test_data)
    csv_text = output.getvalue()
    print(f"Generated CSV text: {len(csv_text)} bytes")
    
    # Benchmark writes
    print("\n" + "-"*60)
    print("WRITE PERFORMANCE")
    print("-"*60)
    custom_write_time = benchmark_write(test_data, CustomCsvWriter, iterations=3)
    std_write_time = benchmark_write(test_data, csv.writer, iterations=3)
    
    print(f"CustomCsvWriter: {custom_write_time:.6f}s")
    print(f"csv.writer:      {std_write_time:.6f}s")
    print(f"Ratio: {custom_write_time/std_write_time:.2f}x slower")
    
    # Benchmark reads
    print("\n" + "-"*60)
    print("READ PERFORMANCE")
    print("-"*60)
    custom_read_time = benchmark_read(csv_text, CustomCsvReader, iterations=3)
    std_read_time = benchmark_read(csv_text, csv.reader, iterations=3)
    
    print(f"CustomCsvReader: {custom_read_time:.6f}s")
    print(f"csv.reader:      {std_read_time:.6f}s")
    print(f"Ratio: {custom_read_time/std_read_time:.2f}x slower")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\nCustom implementation is {custom_write_time/std_write_time:.2f}x slower for writing")
    print(f"Custom implementation is {custom_read_time/std_read_time:.2f}x slower for reading")
    print("\nNote: The custom implementation prioritizes clarity and")
    print("correctness over performance. Python's csv module is")
    print("implemented in C and heavily optimized.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
