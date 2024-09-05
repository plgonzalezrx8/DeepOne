import pytest
import tempfile
import os
from deepOne import expand, process_file

def test_expand_cidr():
    print("\nTesting CIDR expansion")
    result = expand("192.168.1.0/30")
    assert result == ["192.168.1.0", "192.168.1.1", "192.168.1.2", "192.168.1.3"]
    print("CIDR expansion test passed")

def test_expand_last_octet():
    print("\nTesting last octet expansion")
    result = expand("192.168.1.1-3")
    assert result == ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
    print("Last octet expansion test passed")

def test_expand_all_octets():
    print("\nTesting full IP range expansion")
    result = expand("192.168.1.254-192.168.2.2")
    assert result == ["192.168.1.254", "192.168.1.255", "192.168.2.0", "192.168.2.1", "192.168.2.2"]
    print("Full IP range expansion test passed")

def test_expand_single_ip():
    print("\nTesting single IP expansion")
    result = expand("192.168.1.1")
    assert result == ["192.168.1.1"]
    print("Single IP expansion test passed")

def test_expand_invalid_ip():
    print("\nTesting invalid IP handling")
    result = expand("invalid_ip")
    assert result == []
    print("Invalid IP handling test passed")

def test_process_file():
    print("\nTesting file processing")
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as input_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False) as output_file:
        
        input_file.write("192.168.1.0/31\n")
        input_file.write("192.168.1.2-3\n")
        input_file.flush()

        exclude_set = set(["192.168.1.1"])
        process_file(input_file.name, exclude_set, output_file.name)

        output_file.seek(0)
        result = output_file.read().splitlines()

    assert result == ["192.168.1.0", "192.168.1.2", "192.168.1.3"]
    print("File processing test passed")

    # Clean up temporary files
    os.unlink(input_file.name)
    os.unlink(output_file.name)