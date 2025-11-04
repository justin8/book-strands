import os
import tempfile
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from book_strands.cli import cli


def test_help_works_without_config():
    """Test that --help works even when config file doesn't exist."""
    runner = CliRunner()
    
    # Mock the config file path to a non-existent location
    with patch('book_strands.utils.CONFIG_FILE_PATH', '~/.config/nonexistent-config.conf'):
        result = runner.invoke(cli, ['--help'])
        
    assert result.exit_code == 0
    assert "Book Strands CLI tool" in result.output


def test_command_fails_without_config():
    """Test that commands fail with proper error when config file doesn't exist."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock the config file path to a non-existent location
        with patch('book_strands.utils.CONFIG_FILE_PATH', '~/.config/nonexistent-config.conf'):
            result = runner.invoke(cli, ['agent', temp_dir, 'test query'])
            
        assert result.exit_code == 1
        assert "ERROR:" in result.output
        assert "Config file not found" in result.output
        assert "A configuration file is required" in result.output
        assert "Example configuration file content:" in result.output
        assert "[zlib-logins]" in result.output
        assert "user@example.com = password123" in result.output


def test_import_command_fails_without_config():
    """Test that import-local-books command fails with proper error when config file doesn't exist."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a dummy input directory
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)
        
        # Mock the config file path to a non-existent location
        with patch('book_strands.utils.CONFIG_FILE_PATH', '~/.config/nonexistent-config.conf'):
            result = runner.invoke(cli, ['import-local-books', input_dir, temp_dir])
            
        assert result.exit_code == 1
        assert "ERROR:" in result.output
        assert "Config file not found" in result.output
        assert "A configuration file is required" in result.output
        assert "Example configuration file content:" in result.output
        assert "[zlib-logins]" in result.output
        assert "user@example.com = password123" in result.output