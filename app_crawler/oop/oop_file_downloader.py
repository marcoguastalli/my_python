
"""
Object-oriented implementation of file downloader using wget.
Downloads files with comprehensive error handling and progress tracking.
"""

import logging
import subprocess
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import time

#from config.settings import CrawlerConfig
#from oop.app_get_links_oop import ExtractedLink
#from utils.logger import LoggedOperation, log_step, log_download_result, log_progress, log_critical_error

from config.settings import CrawlerConfig
from .oop_link_extractor import ExtractedLink  # Fixed filename
from utils.logger import LoggedOperation, log_step, log_download_result, log_progress, log_critical_error  # Fixed path

@dataclass
class DownloadResult:
    """Data class representing a download operation result."""
    url: str
    filename: str
    success: bool
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    error_message: Optional[str] = None
    wget_exit_code: Optional[int] = None
    download_time: Optional[float] = None


class FileDownloader:
    """Downloads files using wget with comprehensive error handling."""
    
    def __init__(self, config: CrawlerConfig, logger: logging.Logger):
        """Initialize file downloader.
        
        Args:
            config: Crawler configuration
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self._validate_dependencies()
    
    def _validate_dependencies(self):
        """Validate that wget is available on the system."""
        if not shutil.which('wget'):
            error_msg = "wget command not found. Please install wget to use this downloader."
            log_critical_error(self.logger, "dependency check", ValueError(error_msg))
            raise ValueError(error_msg)
        
        log_step(self.logger, "Dependencies validated", "wget available")
    
    def download_files(self, links: List[ExtractedLink]) -> Dict[str, Any]:
        """Download all files in the links list.
        
        Args:
            links: List of ExtractedLink objects to download
            
        Returns:
            Dict[str, Any]: Download summary with results
        """
        if not links:
            self.logger.warning("No links provided for download")
            return self._create_summary([], 0, 0, 0)
        
        with LoggedOperation(self.logger, f"batch download of {len(links)} files"):
            
            self.logger.info(f"Starting download of {len(links)} files to {self.config.target_folder}")
            
            results = []
            successful_downloads = 0
            failed_downloads = 0
            total_size = 0
            
            for i, link in enumerate(links, 1):
                log_progress(self.logger, i, len(links), "files")
                
                result = self._download_single_file(link)
                results.append(result)
                
                if result.success:
                    successful_downloads += 1
                    if result.file_size:
                        total_size += result.file_size
                    self.logger.info(f"✓ Downloaded: {result.filename}")
                else:
                    failed_downloads += 1
                    self.logger.error(f"✗ Failed: {result.filename} - {result.error_message}")
                    
                    # Stop on error if configured
                    if self.config.fail_on_error:
                        error_msg = f"Download failed and FAIL_ON_ERROR is enabled: {result.error_message}"
                        log_critical_error(self.logger, "batch download", RuntimeError(error_msg))
                        break
            
            return self._create_summary(results, successful_downloads, failed_downloads, total_size)
    
    def _download_single_file(self, link: ExtractedLink) -> DownloadResult:
        """Download a single file using wget.
        
        Args:
            link: ExtractedLink object to download
            
        Returns:
            DownloadResult: Result of the download operation
        """
        start_time = time.time()
        
        with LoggedOperation(self.logger, f"download of {link.filename}"):
            
            # Prepare file path
            target_file_path = os.path.join(self.config.target_folder, link.filename)
            
            # Check if file already exists
            if os.path.exists(target_file_path):
                self.logger.debug(f"File already exists: {target_file_path}")
                return DownloadResult(
                    url=link.url,
                    filename=link.filename,
                    success=True,
                    file_path=target_file_path,
                    file_size=os.path.getsize(target_file_path),
                    error_message="File already exists",
                    download_time=time.time() - start_time
                )
            
            # Build wget command
            wget_cmd = self._build_wget_command(link, target_file_path)
            
            try:
                # Execute wget
                result = subprocess.run(
                    wget_cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.config.timeout_in_seconds + 30  # Extra buffer for wget
                )
                
                download_time = time.time() - start_time
                
                # Process result
                return self._process_wget_result(
                    result, link, target_file_path, download_time
                )
                
            except subprocess.TimeoutExpired:
                error_msg = f"Download timed out after {self.config.timeout_in_seconds + 30} seconds"
                log_download_result(self.logger, link.url, False, error_msg=error_msg)
                return DownloadResult(
                    url=link.url,
                    filename=link.filename,
                    success=False,
                    error_message=error_msg,
                    wget_exit_code=-1,
                    download_time=time.time() - start_time
                )
                
            except Exception as e:
                error_msg = f"Unexpected error during download: {e}"
                log_download_result(self.logger, link.url, False, error_msg=error_msg)
                return DownloadResult(
                    url=link.url,
                    filename=link.filename,
                    success=False,
                    error_message=error_msg,
                    download_time=time.time() - start_time
                )
    
    def _build_wget_command(self, link: ExtractedLink, target_path: str) -> List[str]:
        """Build wget command with appropriate options.
        
        Args:
            link: Link to download
            target_path: Target file path
            
        Returns:
            List[str]: wget command as list
        """
        cmd = [
            'wget',
            '--timeout', str(self.config.timeout_in_seconds),
            '--tries', '3',  # Retry 3 times
            '--wait', '1',   # Wait 1 second between retries
            '--random-wait', # Randomize wait time
            '--user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            '--no-check-certificate',  # Handle SSL issues
            '--content-disposition',   # Use server-suggested filename
            '--trust-server-names',    # Trust server names
            '--output-document', target_path,
            link.url
        ]
        
        log_step(self.logger, "wget command built", f"target={target_path}")
        self.logger.debug(f"wget command: {' '.join(cmd)}")
        
        return cmd
    
    def _process_wget_result(self, result: subprocess.CompletedProcess, 
                           link: ExtractedLink, target_path: str, 
                           download_time: float) -> DownloadResult:
        """Process wget subprocess result.
        
        Args:
            result: Subprocess result
            link: Original link
            target_path: Target file path
            download_time: Time taken for download
            
        Returns:
            DownloadResult: Processed download result
        """
        exit_code = result.returncode
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        # Log wget output for debugging
        if stdout:
            self.logger.debug(f"wget stdout: {stdout}")
        if stderr:
            self.logger.debug(f"wget stderr: {stderr}")
        
        # Check if download was successful
        success = (exit_code == 0) and os.path.exists(target_path)
        
        if success:
            file_size = os.path.getsize(target_path)
            log_download_result(self.logger, link.url, True, filename=link.filename)
            
            return DownloadResult(
                url=link.url,
                filename=link.filename,
                success=True,
                file_path=target_path,
                file_size=file_size,
                wget_exit_code=exit_code,
                download_time=download_time
            )
        else:
            # Parse error message
            error_message = self._parse_wget_error(exit_code, stderr)
            log_download_result(self.logger, link.url, False, error_msg=error_message)
            
            # Clean up failed download file if it exists
            if os.path.exists(target_path):
                try:
                    os.remove(target_path)
                    self.logger.debug(f"Cleaned up failed download file: {target_path}")
                except OSError as e:
                    self.logger.warning(f"Could not clean up failed file {target_path}: {e}")
            
            return DownloadResult(
                url=link.url,
                filename=link.filename,
                success=False,
                error_message=error_message,
                wget_exit_code=exit_code,
                download_time=download_time
            )
    
    def _parse_wget_error(self, exit_code: int, stderr: str) -> str:
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
        
        # Extract more specific error from stderr
        if stderr:
            # Common patterns in wget stderr
            if "404" in stderr or "Not Found" in stderr:
                return "File not found (404)"
            elif "403" in stderr or "Forbidden" in stderr:
                return "Access forbidden (403)"
            elif "timeout" in stderr.lower():
                return "Connection timeout"
            elif "certificate" in stderr.lower():
                return "SSL certificate error"
            elif "connection refused" in stderr.lower():
                return "Connection refused"
            elif "no such host" in stderr.lower():
                return "Host not found"
            else:
                # Include first line of stderr for context
                first_error_line = stderr.split('\n')[0]
                return f"{base_error}: {first_error_line}"
        
        return base_error
    
    def _create_summary(self, results: List[DownloadResult], 
                       successful: int, failed: int, total_size: int) -> Dict[str, Any]:
        """Create download summary.
        
        Args:
            results: List of download results
            successful: Number of successful downloads
            failed: Number of failed downloads
            total_size: Total downloaded size in bytes
            
        Returns:
            Dict[str, Any]: Download summary
        """
        # Separate successful and failed results
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        # Calculate statistics
        total_time = sum(r.download_time or 0 for r in results)
        avg_time = total_time / len(results) if results else 0
        
        summary = {
            "status": "completed",
            "total_files": len(results),
            "successful_downloads": successful,
            "failed_downloads": failed,
            "success_rate": (successful / len(results) * 100) if results else 0,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_time_seconds": round(total_time, 2),
            "average_time_per_file": round(avg_time, 2),
            "target_folder": self.config.target_folder,
            "downloaded_files": [
                {
                    "url": r.url,
                    "filename": r.filename,
                    "file_path": r.file_path,
                    "size_bytes": r.file_size,
                    "download_time": r.download_time
                }
                for r in successful_results
            ],
            "failed_files": [
                {
                    "url": r.url,
                    "filename": r.filename,
                    "error_message": r.error_message,
                    "wget_exit_code": r.wget_exit_code
                }
                for r in failed_results
            ]
        }
        
        # Log summary
        self.logger.info(f"Download summary: {successful}/{len(results)} successful, "
                        f"{summary['total_size_mb']}MB downloaded in {summary['total_time_seconds']}s")
        
        return summary