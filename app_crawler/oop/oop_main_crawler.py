#!/usr/bin/env python3
"""
Main PDF crawler application using Object-Oriented Programming approach.
Coordinates link extraction and file downloading with comprehensive error handling.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import ConfigManager, CrawlerConfig
from utils.logger import setup_application_logging, log_step, log_critical_error, LoggedOperation
from .oop_link_extractor import LinkExtractor
from .oop_file_downloader import FileDownloader


class PDFCrawler:
    """Main PDF crawler orchestrator using OOP approach."""
    
    def __init__(self, env_file: str = '.env'):
        """Initialize PDF crawler.
        
        Args:
            env_file: Path to environment configuration file
        """
        self.env_file = env_file
        self.config: CrawlerConfig = None
        self.logger: logging.Logger = None
        self.link_extractor: LinkExtractor = None
        self.file_downloader: FileDownloader = None
    
    def initialize(self):
        """Initialize all crawler components.
        
        Raises:
            Exception: If initialization fails
        """
        with LoggedOperation(logging.getLogger('init'), "crawler initialization"):
            
            # Load configuration
            self._load_configuration()
            
            # Setup logging
            self._setup_logging()
            
            # Initialize components
            self._initialize_components()
            
            log_step(self.logger, "Crawler initialized successfully")
    
    def _load_configuration(self):
        """Load and validate configuration from .env file."""
        try:
            config_manager = ConfigManager(self.env_file)
            self.config = config_manager.load_config()
        except Exception as e:
            print(f"CRITICAL: Configuration loading failed: {e}")
            raise
    
    def _setup_logging(self):
        """Setup application logging based on configuration."""
        try:
            self.logger = setup_application_logging(
                log_level=self.config.log_level,
                log_file=self.config.log_file
            )
            self.logger.info("=== PDF Crawler Started (OOP Implementation) ===")
        except Exception as e:
            print(f"CRITICAL: Logging setup failed: {e}")
            raise
    
    def _initialize_components(self):
        """Initialize crawler components."""
        self.link_extractor = LinkExtractor(self.config, self.logger)
        self.file_downloader = FileDownloader(self.config, self.logger)
    
    def crawl_and_download(self) -> Dict[str, Any]:
        """Execute the complete crawl and download process.
        
        Returns:
            Dict[str, Any]: Complete operation results
            
        Raises:
            Exception: If critical error occurs during processing
        """
        with LoggedOperation(self.logger, "complete crawl and download operation"):
            
            log_step(self.logger, "Starting PDF crawl and download", 
                    f"endpoint={self.config.endpoint}, extension={self.config.extension}")
            
            try:
                # Phase 1: Extract links
                extracted_links = self._extract_links()
                
                # Phase 2: Download files
                download_results = self._download_files(extracted_links)
                
                # Phase 3: Generate final report
                final_report = self._generate_final_report(extracted_links, download_results)
                
                self.logger.info("=== PDF Crawler Completed Successfully ===")
                return final_report
                
            except Exception as e:
                log_critical_error(self.logger, "crawl and download", e)
                
                # Generate error report
                error_report = self._generate_error_report(e)
                self.logger.error("=== PDF Crawler Failed ===")
                return error_report
    
    def _extract_links(self):
        """Extract links from the target endpoint."""
        log_step(self.logger, "Phase 1: Link extraction", "starting")
        
        with self.link_extractor as extractor:
            links = extractor.extract_links()
            
            if not links:
                self.logger.warning("No links found matching the specified criteria")
                return []
            
            log_step(self.logger, "Phase 1: Link extraction", 
                    f"completed - found {len(links)} links")
            
            # Log link details at DEBUG level
            for i, link in enumerate(links, 1):
                self.logger.debug(f"Link {i}: {link.filename} ({link.url})")
            
            return links
    
    def _download_files(self, links):
        """Download all extracted files."""
        if not links:
            self.logger.info("No files to download")
            return {"status": "no_files", "downloaded_files": [], "failed_files": []}
        
        log_step(self.logger, "Phase 2: File download", 
                f"starting download of {len(links)} files")
        
        download_results = self.file_downloader.download_files(links)
        
        log_step(self.logger, "Phase 2: File download", 
                f"completed - {download_results['successful_downloads']} successful, "
                f"{download_results['failed_downloads']} failed")
        
        return download_results
    
    def _generate_final_report(self, links, download_results) -> Dict[str, Any]:
        """Generate comprehensive final report.
        
        Args:
            links: List of extracted links
            download_results: Download operation results
            
        Returns:
            Dict[str, Any]: Final report
        """
        log_step(self.logger, "Phase 3: Report generation", "creating final report")
        
        report = {
            "crawler_info": {
                "implementation": "Object-Oriented Programming",
                "version": "1.0.0",
                "endpoint": self.config.endpoint,
                "extension": self.config.extension,
                "target_folder": self.config.target_folder
            },
            "extraction_results": {
                "links_found": len(links),
                "links_details": [
                    {
                        "url": link.url,
                        "filename": link.filename,
                        "text": link.text,
                        "size_hint": link.size_hint
                    }
                    for link in links
                ]
            },
            "download_results": download_results,
            "summary": {
                "total_links_found": len(links),
                "files_downloaded": download_results.get("successful_downloads", 0),
                "files_failed": download_results.get("failed_downloads", 0),
                "success_rate_percent": download_results.get("success_rate", 0),
                "total_size_mb": download_results.get("total_size_mb", 0),
                "operation_status": "success"
            }
        }
        
        log_step(self.logger, "Phase 3: Report generation", "completed")
        return report
    
    def _generate_error_report(self, error: Exception) -> Dict[str, Any]:
        """Generate error report when operation fails.
        
        Args:
            error: Exception that caused failure
            
        Returns:
            Dict[str, Any]: Error report
        """
        return {
            "crawler_info": {
                "implementation": "Object-Oriented Programming",
                "version": "1.0.0",
                "endpoint": self.config.endpoint if self.config else "unknown",
                "extension": self.config.extension if self.config else "unknown"
            },
            "extraction_results": {
                "links_found": 0,
                "links_details": []
            },
            "download_results": {
                "status": "error",
                "downloaded_files": [],
                "failed_files": []
            },
            "summary": {
                "total_links_found": 0,
                "files_downloaded": 0,
                "files_failed": 0,
                "success_rate_percent": 0,
                "operation_status": "error",
                "error_message": str(error),
                "error_type": type(error).__name__
            }
        }
    
    def cleanup(self):
        """Clean up crawler resources."""
        if self.link_extractor:
            self.link_extractor.close()
        
        if self.logger:
            log_step(self.logger, "Cleanup completed")


def main():
    """Main entry point for the OOP PDF crawler."""
    crawler = None
    
    try:
        # Initialize crawler
        crawler = PDFCrawler()
        crawler.initialize()
        
        # Execute crawl and download
        results = crawler.crawl_and_download()
        
        # Output results as pretty JSON
        print("\n" + "="*80)
        print("PDF CRAWLER RESULTS (Object-Oriented Programming)")
        print("="*80)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # Determine exit code
        if results["summary"]["operation_status"] == "success":
            return 0
        else:
            return 1
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
    
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        return 1
    
    finally:
        if crawler:
            crawler.cleanup()


if __name__ == "__main__":
    sys.exit(main())
