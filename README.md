# DeepOne

DeepOne is a Python tool designed to expand, exclude, and split multiple IP range formats. It's particularly useful for network administrators and security professionals who need to manage large lists of IP addresses.

## Features

- Expands various IP range formats into individual IP addresses
- Excludes specified IP addresses or ranges from the output
- Splits the resulting IP list into multiple files
- Supports multiple input formats for flexibility

## Supported IP Range Formats

DeepOne can handle the following IP range formats:

1. CIDR notation (e.g., 192.168.3.0/24)
2. Last octet range (e.g., 192.168.3.0-255)
3. Full IP range (e.g., 192.168.3.0-192.168.4.155)
4. Single IP addresses (e.g., 192.168.3.1)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/DeepOne.git
   cd DeepOne
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

python deepOne.py [-h] -i INPUT [-e EXCLUDE] [-o OUTPUT] [-s SPLIT]

### Options

| Option | Description |
|--------|-------------|
| -i, --input | Path to input file (required) |
| -e, --exclude | Path to exclude file |
| -o, --output | Name of output file (default: ./output.txt) |
| -s, --split | Number of files to split output into (default: 1) |
| -h, --help | Show help message and exit |

### Input File Format

The input file should contain one IP range per line, using any of the supported formats mentioned above.

### Exclude File Format

The exclude file should contain IP addresses or ranges to be excluded from the final output, one per line. It supports the same formats as the input file.

## Examples

1. Basic usage:

   ```
   python deepOne.py -i input.txt -o output.txt
   ```

2. Using an exclude file:

   ```
   python deepOne.py -i input.txt -e exclude.txt -o output.txt
   ```

3. Splitting the output into multiple files:

   ```
   python deepOne.py -i input.txt -o output.txt -s 5
   ```

## How It Works

1. The script reads the input file and expands each IP range into individual IP addresses.
2. If an exclude file is provided, it expands the exclusions and removes them from the result set.
3. The script writes the resulting IP addresses to the output file.
4. If splitting is requested, it divides the output into the specified number of files.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
