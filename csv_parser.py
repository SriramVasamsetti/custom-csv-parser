"""Custom CSV Parser Implementation.

This module provides custom CSV reader and writer classes that implement
CSV parsing from scratch without relying on Python's built-in csv module.
"""


class CustomCsvReader:
    """A custom CSV reader that parses CSV files character-by-character.
    
    Implements the iterator protocol to yield rows as lists of strings.
    Handles quoted fields, escaped quotes, and embedded newlines.
    """
    
    def __init__(self, fileobj, delimiter=',', quotechar='"'):
        """Initialize the CSV reader.
        
        Args:
            fileobj: File object opened in text mode
            delimiter: Field separator (default: ',')
            quotechar: Quote character (default: '"')
        """
        self.fileobj = fileobj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.buffer = ""
        self.eof = False
    
    def __iter__(self):
        """Return the iterator object (self)."""
        return self
    
    def __next__(self):
        """Parse and return the next row as a list of strings.
        
        Raises:
            StopIteration: When end of file is reached
        """
        if self.eof and not self.buffer:
            raise StopIteration
        
        row = []
        current_field = ""
        in_quotes = False
        
        while True:
            # Read character by character
            if not self.buffer:
                chunk = self.fileobj.read(4096)
                if not chunk:
                    self.eof = True
                    if current_field or in_quotes:
                        row.append(current_field)
                    if row:
                        return row
                    raise StopIteration
                self.buffer = chunk
            
            char = self.buffer[0]
            self.buffer = self.buffer[1:]
            
            # Handle quote character
            if char == self.quotechar:
                if in_quotes:
                    # Check for escaped quote
                    if self.buffer and self.buffer[0] == self.quotechar:
                        current_field += self.quotechar
                        self.buffer = self.buffer[1:]
                    else:
                        in_quotes = False
                else:
                    in_quotes = True
            # Handle delimiter
            elif char == self.delimiter and not in_quotes:
                row.append(current_field)
                current_field = ""
            # Handle newline (end of row)
            elif char in ('\n', '\r') and not in_quotes:
                row.append(current_field)
                # Handle CRLF
                if char == '\r' and self.buffer and self.buffer[0] == '\n':
                    self.buffer = self.buffer[1:]
                return row
            else:
                current_field += char
    
    def read(self):
        """Read all remaining rows and return them as a list."""
        return list(self)


class CustomCsvWriter:
    """A custom CSV writer that writes data to CSV format.
    
    Handles quoting and escaping of fields automatically.
    """
    
    def __init__(self, fileobj, delimiter=',', quotechar='"'):
        """Initialize the CSV writer.
        
        Args:
            fileobj: File object opened in text mode
            delimiter: Field separator (default: ',')
            quotechar: Quote character (default: '"')
        """
        self.fileobj = fileobj
        self.delimiter = delimiter
        self.quotechar = quotechar
    
    def _needs_quoting(self, field):
        """Check if a field needs to be quoted.
        
        A field needs quoting if it contains:
        - The delimiter
        - The quote character
        - Newline characters
        
        Args:
            field: String field to check
            
        Returns:
            bool: True if field needs quoting, False otherwise
        """
        return (self.delimiter in field or 
                self.quotechar in field or 
                '\n' in field or 
                '\r' in field)
    
    def _escape_field(self, field):
        """Escape and quote a field if necessary.
        
        Args:
            field: String field to escape
            
        Returns:
            str: Properly escaped field
        """
        if self._needs_quoting(field):
            # Escape quotes by doubling them
            escaped = field.replace(self.quotechar, self.quotechar + self.quotechar)
            return self.quotechar + escaped + self.quotechar
        return field
    
    def writerow(self, row):
        """Write a single row to the CSV file.
        
        Args:
            row: List of fields (strings or convertible to strings)
        """
        # Convert all fields to strings and escape them
        escaped_fields = [self._escape_field(str(field)) for field in row]
        line = self.delimiter.join(escaped_fields) + '\n'
        self.fileobj.write(line)
    
    def writerows(self, rows):
        """Write multiple rows to the CSV file.
        
        Args:
            rows: List of rows, where each row is a list of fields
        """
        for row in rows:
            self.writerow(row)
