"""
Functional programming implementation of file downloader using wget.
Pure functions for downloading files with comprehensive error handling.
"""

import logging
import subprocess
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Callable
import time
from functools import partial

from config.settings import CrawlerConfig
from utils.logger import log_step, log_download_result, log_progress, log_critical_error


def validate_wget_available() -> bool:
    """Check if wget is available on the system.
    
    Returns:
        bool: True if wget is available
    """
    return shutil.which('wget') is not None


def build_wget_command(url: str, target_path: str, timeout: int) -> List[str]:
    """Build wget command with appropriate options.
    
    Args:
        url: URL to download
        target_path: Target file path
        timeout: Timeout in seconds
        
    Returns:
        List[str]: wget command as list
    """
    return [
        'wget',
        '--timeout', str(timeout),
        '--tries', '3',
        '--wait', '1',
        '--random-wait',
        '--user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        '--no-check-certificate',
        '--content-disposition',
        '--trust-server-names',
        '--output-document', target_path,
        url
    ]


def parse_wget_error(exit_code: int, stderr: str) -> str:
    """Parse wget error message based on exit code and stderr.
    
    Args:
        exit_code: wget exit code
        stderr: wget stderr output
        
    Returns:
        str: Human-readable error message
    """
    # Common wget exit codes
    error_messages = {
        1: "Generic error",
        2: "Parse error (command line)",
        3: "File I/O error",
        4: "Network failure",
        5: "SSL verification failure",
        6: "Username/password authentication failure",
        7: "Protocol errors",
        8: "Server issued an error response"
    }
    
    base_error = error_messages.get(exit_code, f"Unknown error (exit code {exit_code})")
    
    if stderr:
        # Extract specific error patterns
        stderr_lower = stderr.lower()
        if "404" in stderr or "not found" in stderr_lower:
            return "File not found (404)"
        elif "403" in stderr or "forbidden" in stderr_lower:
            return "Access forbidden (403)"
        elif "timeout" in stderr_lower:
            return "Connection timeout"
        elif "certificate" in stderr_lower:
            return "SSL certificate error"
        elif "connection refused" in stderr_lower:
            return "Connection refused"
        elif "no such host" in stderr_lower:
            return "Host not found"
        else:
            first_error_line = stderr.split('\n')[0]
            return f"{base_error}: {first_error_line}"
    
    return base_error


def execute_wget_command(cmd: List[str], timeout: int) -> Tuple[int, str, str]:
    """Execute wget command with timeout handling.
    
    Args:
        cmd: wget command as list
        timeout: Timeout in seconds
        
    Returns:
        Tuple[int, str, str]: (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30  # Extra buffer for wget
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    
    except subprocess.TimeoutExpired:
        return -1, "", f"Download timed out after {timeout + 30} seconds"


def check_file_exists(file_path: str) -> Tuple[bool, Optional[int]]:
    """Check if file exists and get its size.
    
    Args:
        file_path: Path to check
        
    Returns:
        Tuple[bool, Optional[int]]: (exists, size_in_bytes)
    """
    if os.path.exists(file_path):
        try:
            size = os.path.getsize(file_path)
            return True, size
        except OSError:
            return True, None
    return False, None


def clean_up_failed_file(file_path: str, logger: logging.Logger) -> None:
    """Clean up a failed download file.
    
    Args:
        file_path: Path to clean up
        logger: Logger instance
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Cleaned up failed download file: {file_path}")
    except OSError as e:
        logger.warning(f"Could not clean up failed file {file_path}: {e}")


def create_download_result(url: str, 
                         filename: str, 
                         success: bool, 
                         file_path: Optional[str] = None,
                         file_size: Optional[int] = None,
                         error_message: Optional[str] = None,
                         wget_exit_code: Optional[int] = None,
                         download_time: Optional[float] = None) -> Dict[str, Any]:
    """Create a download result dictionary.
    
    Args:
        url: Downloaded URL
        filename: Target filename
        success: Whether download was successful
        file_path: Path to downloaded file (if successful)
        file_size: File size in bytes (if successful)
        error_message: Error message (if failed)
        wget_exit_code: wget exit code
        download_time: Time taken for download
        
    Returns:
        Dict[str, Any]: Download result
    """
    return {
        'url': url,
        'filename': filename,
        'success': success,
        'file_path': file_path,
        'file_size': file_size,
        'error_message': error_message,
        'wget_exit_code': wget_exit_code,
        'download_time': download_time
    }


def download_single_file(url: str, 
                        filename: str, 
                        target_folder: str, 
                        timeout: int, 
                        logger: logging.Logger) -> Dict[str, Any]:
    """Download a single file using wget (pure function approach).
    
    Args:
        url: URL to download
        filename: Target filename
        target_folder: Target directory
        timeout: Timeout in seconds
        logger: Logger instance
        
    Returns:
        Dict[str, Any]: Download result
    """
    start_time = time.time()
    target_path = os.path.join(target_folder, filename)
    
    log_step(logger, "Starting single file download", f"url={url}, target={filename}")
    
    # Check if file already exists
    file_exists, existing_size = check_file_exists(target_path)
    if file_exists:
        logger.debug(f"File already exists: {target_path}")
        return create_download_result(
            url=url,
            filename=filename,
            success=True,
            file_path=target_path,
            file_size=existing_size,
            error_message="File already exists",
            download_time=time.time() - start_time
        )
    
    # Build and execute wget command
    wget_cmd = build_wget_command(url, target_path, timeout)
    logger.debug(f"wget command: {' '.join(wget_cmd)}")
    
    exit_code, stdout, stderr = execute_wget_command(wget_cmd, timeout)
    download_time = time.time() - start_time
    
    # Log wget output
    if stdout:
        logger.debug(f"wget stdout: {stdout}")
    if stderr:
        logger.debug(f"wget stderr: {stderr}")
    
    # Check download success
    file_exists_after, final_size = check_file_exists(target_path)
    success = (exit_code == 0) and file_exists_after
    
    if success:
        log_download_result(logger, url, True, filename=filename)
        return create_download_result(
            url=url,
            filename=filename,
            success=True,
            file_path=target_path,
            file_size=final_size,
            wget_exit_code=exit_code,
            download_time=download_time
        )
    else:
        # Handle failure
        error_message = parse_wget_error(exit_code, stderr)
        log_download_result(logger, url, False, error_msg=error_message)
        
        # Clean up failed file
        clean_up_failed_file(target_path, logger)
        
        return create_download_result(
            url=url,
            filename=filename,
            success=False,
            error_message=error_message,
            wget_exit_code=exit_code,
            download_time=download_time
        )


def should_continue_on_failure(fail_on_error: bool, result: Dict[str, Any]) -> bool:
    """Determine if download process should continue after a failure.
    
    Args:
        fail_on_error: Configuration setting
        result: Download result
        
    Returns:
        bool: True if should continue, False if should stop
    """
    if result['success']:
        return True
    
    return not fail_on_error


def download_files_batch(links: List[Dict[str, Any]], 
                        target_folder: str, 
                        timeout: int, 
                        fail_on_error: bool, 
                        logger: logging.Logger) -> List[Dict[str, Any]]:
    """Download a batch of files (functional approach with early termination).
    
    Args:
        links: List of link dictionaries
        target_folder: Target download directory
        timeout: Timeout per file
        fail_on_error: Whether to stop on first error
        logger: Logger instance
        
    Returns:
        List[Dict[str, Any]]: List of download results
    """
    if not links:
        logger.warning("No links provided for download")
        return []
    
    log_step(logger, "Starting batch download", f"files={len(links)}, target={target_folder}")
    
    results = []
    
    for i, link in enumerate(links, 1):
        log_progress(logger, i, len(links), "files")
        
        # Extract link data
        url = link['url']
        filename = link['filename']
        
        # Download single file
        result = download_single_file(url, filename, target_folder, timeout, logger)
        results.append(result)
        
        # Log result
        if result['success']:
            logger.info(f"✓ Downloaded: {filename}")
        else:
            logger.error(f"✗ Failed: {filename} - {result['error_message']}")
        
        # Check if should continue
        if not should_continue_on_failure(fail_on_error, result):
            error_msg = f"Download failed and FAIL_ON_ERROR is enabled: {result['error_message']}"
            log_critical_error(logger, "batch download", RuntimeError(error_msg))
            break
    
    return results


def calculate_download_statistics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate download statistics from results.
    
    Args:
        results: List of download results
        
    Returns:
        Dict[str, Any]: Download statistics
    """
    if not results:
        return {
            'total_files': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'success_rate': 0,
            'total_size_bytes': 0,
            'total_time_seconds': 0,
            'average_time_per_file': 0
        }
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    total_size = sum(r.get('file_size', 0) or 0 for r in successful)
    total_time = sum(r.get('download_time', 0) or 0 for r in results)
    
    return {
        'total_files': len(results),
        'successful_downloads': len(successful),
        'failed_downloads': len(failed),
        'success_rate': (len(successful) / len(results) * 100) if results else 0,
        'total_size_bytes': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'total_time_seconds': round(total_time, 2),
        'average_time_per_file': round(total_time / len(results), 2) if results else 0
    }


def partition_results(results: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Partition results into successful and failed downloads.
    
    Args:
        results: List of download results
        
    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: (successful, failed)
    """
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    return successful, failed


def format_successful_file_info(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format successful download info for summary.
    
    Args:
        result: Download result
        
    Returns:
        Dict[str, Any]: Formatted file info
    """
    return {
        'url': result['url'],
        'filename': result['filename'],
        'file_path': result['file_path'],
        'size_bytes': result['file_size'],
        'download_time': result['download_time']
    }


def format_failed_file_info(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format failed download info for summary.
    
    Args:
        result: Download result
        
    Returns:
        Dict[str, Any]: Formatted error info
    """
    return {
        'url': result['url'],
        'filename': result['filename'],
        'error_message': result['error_message'],
        'wget_exit_code': result['wget_exit_code']
    }


def create_download_summary(results: List[Dict[str, Any]], 
                          target_folder: str, 
                          logger: logging.Logger) -> Dict[str, Any]:
    """Create comprehensive download summary.
    
    Args:
        results: List of download results
        target_folder: Target download directory
        logger: Logger instance
        
    Returns:
        Dict[str, Any]: Download summary
    """
    # Calculate statistics
    stats = calculate_download_statistics(results)
    
    # Partition results
    successful, failed = partition_results(results)
    
    # Create summary
    summary = {
        'status': 'completed',
        **stats,
        'target_folder': target_folder,
        'downloaded_files': [format_successful_file_info(r) for r in successful],
        'failed_files': [format_failed_file_info(r) for r in failed]
    }
    
    # Log summary
    logger.info(f"Download summary: {stats['successful_downloads']}/{stats['total_files']} successful, "
               f"{stats['total_size_mb']}MB downloaded in {stats['total_time_seconds']}s")
    
    return summary


# Main download function
def download_files_from_links(links: List[Dict[str, Any]], 
                            config: CrawlerConfig, 
                            logger: logging.Logger) -> Dict[str, Any]:
    """Main function to download files from links using functional approach.
    
    Args:
        links: List of link dictionaries
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Dict[str, Any]: Download summary
        
    Raises:
        ValueError: If wget is not available
    """
    log_step(logger, "Starting file downloads", f"count={len(links)}")
    
    # Validate dependencies
    if not validate_wget_available():
        error_msg = "wget command not found. Please install wget to use this downloader."
        log_critical_error(logger, "dependency check", ValueError(error_msg))
        raise ValueError(error_msg)
    
    # Execute downloads
    results = download_files_batch(
        links=links,
        target_folder=config.target_folder,
        timeout=config.timeout_in_seconds,
        fail_on_error=config.fail_on_error,
        logger=logger
    )
    
    # Create and return summary
    return create_download_summary(results, config.target_folder, logger)


# Higher-order functions for advanced processing
def apply_download_filter(filter_func: Callable[[Dict[str, Any]], bool], 
                         links: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply a filter function to links before downloading.
    
    Args:
        filter_func: Function that takes a link dict and returns bool
        links: List of link dictionaries
        
    Returns:
        List[Dict[str, Any]]: Filtered links
    """
    return [link for link in links if filter_func(link)]


def create_size_filter(min_size_mb: float = 0, max_size_mb: float = float('inf')):
    """Create a filter based on estimated file size.
    
    Args:
        min_size_mb: Minimum size in MB
        max_size_mb: Maximum size in MB
        
    Returns:
        Callable: Filter function
    """
    def size_filter(link: Dict[str, Any]) -> bool:
        size_hint = link.get('size_hint', '')
        if not size_hint or 'MB' not in size_hint.upper():
            return True  # Allow links without size hints
        
        try:
            import re
            match = re.search(r'(\d+\.?\d*)', size_hint)
            if match:
                size_mb = float(match.group(1))
                return min_size_mb <= size_mb <= max_size_mb
        except (ValueError, AttributeError):
            pass
        
        return True  # Allow if size parsing fails
    
    return size_filter


# Safe download function with comprehensive error handling
def download_files_safe(links: List[Dict[str, Any]], 
                       config: CrawlerConfig, 
                       logger: logging.Logger) -> Tuple[Dict[str, Any], Optional[str]]:
    """Safely download files with comprehensive error handling.
    
    Args:
        links: List of link dictionaries
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Tuple[Dict[str, Any], Optional[str]]: (download_summary, error_message)
    """
    try:
        summary = download_files_from_links(links, config, logger)
        return summary, None
    
    except ValueError as e:
        error_msg = f"Configuration error during download: {e}"
        log_critical_error(logger, "file download", e)
        return {'status': 'error', 'downloaded_files': [], 'failed_files': []}, error_msg
    
    except Exception as e:
        error_msg = f"Unexpected error during download: {e}"
        log_critical_error(logger, "file download", e)
        return {'status': 'error', 'downloaded_files': [], 'failed_files': []}, error_msg
