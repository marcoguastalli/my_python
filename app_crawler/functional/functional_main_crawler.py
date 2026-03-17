#!/usr/bin/env python3
"""
Main PDF crawler application using Functional Programming approach.
Pure functions for coordinating link extraction and file downloading.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import ConfigManager, CrawlerConfig
from utils.logger import setup_application_logging, log_step, log_critical_error
from functional.app_get_links_functional import extract_links_safe
from functional.app_wget_links_functional import download_files_safe


def load_and_validate_config(env_file: str = '.env') -> Tuple[Optional[CrawlerConfig], Optional[str]]:
    """Load and validate configuration from .env file.
    
    Args:
        env_file: Path to environment file
        
    Returns:
        Tuple[Optional[CrawlerConfig], Optional[str]]: (config, error_message)
    """
    try:
        config_manager = ConfigManager(env_file)
        config = config_manager.load_config()
        return config, None
    except Exception as e:
        return None, f"Configuration loading failed: {e}"


def initialize_logging(config: CrawlerConfig) -> Tuple[Optional[logging.Logger], Optional[str]]:
    """Initialize application logging.
    
    Args:
        config: Crawler configuration
        
    Returns:
        Tuple[Optional[logging.Logger], Optional[str]]: (logger, error_message)
    """
    try:
        logger = setup_application_logging(
            log_level=config.log_level,
            log_file=config.log_file
        )
        logger.info("=== PDF Crawler Started (Functional Programming Implementation) ===")
        return logger, None
    except Exception as e:
        return None, f"Logging setup failed: {e}"


def execute_crawl_phase(config: CrawlerConfig, logger: logging.Logger) -> Tuple[list, Optional[str]]:
    """Execute the link extraction phase.
    
    Args:
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Tuple[list, Optional[str]]: (extracted_links, error_message)
    """
    log_step(logger, "Phase 1: Link extraction", "starting")
    
    links, error = extract_links_safe(config, logger)
    
    if error:
        return [], error
    
    if not links:
        logger.warning("No links found matching the specified criteria")
        log_step(logger, "Phase 1: Link extraction", "completed - no links found")
        return [], None
    
    log_step(logger, "Phase 1: Link extraction", f"completed - found {len(links)} links")
    
    # Log link details at DEBUG level
    for i, link in enumerate(links, 1):
        logger.debug(f"Link {i}: {link['filename']} ({link['url']})")
    
    return links, None


def execute_download_phase(links: list, config: CrawlerConfig, logger: logging.Logger) -> Tuple[Dict[str, Any], Optional[str]]:
    """Execute the file download phase.
    
    Args:
        links: List of extracted links
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Tuple[Dict[str, Any], Optional[str]]: (download_results, error_message)
    """
    if not links:
        logger.info("No files to download")
        return {
            "status": "no_files",
            "total_files": 0,
            "successful_downloads": 0,
            "failed_downloads": 0,
            "downloaded_files": [],
            "failed_files": []
        }, None
    
    log_step(logger, "Phase 2: File download", f"starting download of {len(links)} files")
    
    download_results, error = download_files_safe(links, config, logger)
    
    if error:
        return download_results, error
    
    log_step(logger, "Phase 2: File download", 
            f"completed - {download_results.get('successful_downloads', 0)} successful, "
            f"{download_results.get('failed_downloads', 0)} failed")
    
    return download_results, None


def create_crawler_info(config: CrawlerConfig) -> Dict[str, Any]:
    """Create crawler information section.
    
    Args:
        config: Crawler configuration
        
    Returns:
        Dict[str, Any]: Crawler info
    """
    return {
        "implementation": "Functional Programming",
        "version": "1.0.0",
        "endpoint": config.endpoint,
        "extension": config.extension,
        "target_folder": config.target_folder
    }


def create_extraction_results(links: list) -> Dict[str, Any]:
    """Create extraction results section.
    
    Args:
        links: List of extracted links
        
    Returns:
        Dict[str, Any]: Extraction results
    """
    return {
        "links_found": len(links),
        "links_details": [
            {
                "url": link['url'],
                "filename": link['filename'],
                "text": link['text'],
                "size_hint": link.get('size_hint')
            }
            for link in links
        ]
    }


def create_operation_summary(links: list, download_results: Dict[str, Any], success: bool, error_msg: Optional[str] = None) -> Dict[str, Any]:
    """Create operation summary section.
    
    Args:
        links: List of extracted links
        download_results: Download operation results
        success: Whether operation was successful
        error_msg: Error message if operation failed
        
    Returns:
        Dict[str, Any]: Operation summary
    """
    summary = {
        "total_links_found": len(links),
        "files_downloaded": download_results.get("successful_downloads", 0),
        "files_failed": download_results.get("failed_downloads", 0),
        "success_rate_percent": download_results.get("success_rate", 0),
        "total_size_mb": download_results.get("total_size_mb", 0),
        "operation_status": "success" if success else "error"
    }
    
    if error_msg:
        summary["error_message"] = error_msg
    
    return summary


def generate_final_report(config: CrawlerConfig, 
                         links: list, 
                         download_results: Dict[str, Any], 
                         success: bool, 
                         error_msg: Optional[str] = None) -> Dict[str, Any]:
    """Generate comprehensive final report.
    
    Args:
        config: Crawler configuration
        links: List of extracted links
        download_results: Download operation results
        success: Whether operation was successful
        error_msg: Error message if operation failed
        
    Returns:
        Dict[str, Any]: Final report
    """
    return {
        "crawler_info": create_crawler_info(config),
        "extraction_results": create_extraction_results(links),
        "download_results": download_results,
        "summary": create_operation_summary(links, download_results, success, error_msg)
    }


def execute_complete_crawl_workflow(config: CrawlerConfig, logger: logging.Logger) -> Dict[str, Any]:
    """Execute the complete crawl and download workflow.
    
    Args:
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Dict[str, Any]: Complete operation results
    """
    log_step(logger, "Starting PDF crawl and download workflow", 
            f"endpoint={config.endpoint}, extension={config.extension}")
    
    # Phase 1: Extract links
    links, extraction_error = execute_crawl_phase(config, logger)
    
    if extraction_error:
        logger.error(f"Link extraction failed: {extraction_error}")
        return generate_final_report(config, [], {}, False, extraction_error)
    
    # Phase 2: Download files
    download_results, download_error = execute_download_phase(links, config, logger)
    
    if download_error:
        logger.error(f"File download failed: {download_error}")
        return generate_final_report(config, links, download_results, False, download_error)
    
    # Phase 3: Generate final report
    log_step(logger, "Phase 3: Report generation", "creating final report")
    final_report = generate_final_report(config, links, download_results, True)
    log_step(logger, "Phase 3: Report generation", "completed")
    
    logger.info("=== PDF Crawler Completed Successfully ===")
    return final_report


def handle_critical_error(error: Exception, config: Optional[CrawlerConfig] = None) -> Dict[str, Any]:
    """Handle critical errors that prevent normal operation.
    
    Args:
        error: Exception that occurred
        config: Crawler configuration (if available)
        
    Returns:
        Dict[str, Any]: Error report
    """
    return {
        "crawler_info": {
            "implementation": "Functional Programming",
            "version": "1.0.0",
            "endpoint": config.endpoint if config else "unknown",
            "extension": config.extension if config else "unknown",
            "target_folder": config.target_folder if config else "unknown"
        },
        "extraction_results": {
            "links_found": 0,
            "links_details": []
        },
        "download_results": {
            "status": "error",
            "total_files": 0,
            "successful_downloads": 0,
            "failed_downloads": 0,
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


def crawl_pdfs_functional(env_file: str = '.env') -> Dict[str, Any]:
    """Main functional PDF crawler implementation.
    
    Args:
        env_file: Path to environment configuration file
        
    Returns:
        Dict[str, Any]: Complete operation results
    """
    # Load configuration
    config, config_error = load_and_validate_config(env_file)
    if config_error:
        print(f"CRITICAL: {config_error}")
        return handle_critical_error(ValueError(config_error))
    
    # Initialize logging
    logger, logging_error = initialize_logging(config)
    if logging_error:
        print(f"CRITICAL: {logging_error}")
        return handle_critical_error(ValueError(logging_error), config)
    
    try:
        # Execute complete workflow
        return execute_complete_crawl_workflow(config, logger)
        
    except Exception as e:
        log_critical_error(logger, "complete workflow", e)
        logger.error("=== PDF Crawler Failed ===")
        return handle_critical_error(e, config)


def main() -> int:
    """Main entry point for the functional PDF crawler.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Execute crawler
        results = crawl_pdfs_functional()
        
        # Output results as pretty JSON
        print("\n" + "="*80)
        print("PDF CRAWLER RESULTS (Functional Programming)")
        print("="*80)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # Determine exit code based on operation status
        operation_status = results.get("summary", {}).get("operation_status", "error")
        return 0 if operation_status == "success" else 1
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
    
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
