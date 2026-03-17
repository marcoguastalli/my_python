"""
Functional programming implementation of link extraction from web pages.
Pure functions for extracting links matching specified file extension using BeautifulSoup.
"""

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set, Optional, Tuple, Any
import time
from functools import reduce

from config.settings import CrawlerConfig
from utils.logger import log_step, log_critical_error


def create_session(config: CrawlerConfig) -> requests.Session:
    """Create and configure a requests session.
    
    Args:
        config: Crawler configuration
        
    Returns:
        requests.Session: Configured session
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    session.timeout = config.timeout_in_seconds
    return session


def fetch_page_content(url: str, session: requests.Session, logger: logging.Logger) -> str:
    """Fetch content from a web page.
    
    Args:
        url: URL to fetch
        session: Configured requests session
        logger: Logger instance
        
    Returns:
        str: HTML content of the page
        
    Raises:
        requests.RequestException: For network-related errors
    """
    log_step(logger, "Fetching webpage", url)
    
    try:
        response = session.get(url)
        response.raise_for_status()
        
        log_step(logger, "Page fetched successfully", 
                f"status={response.status_code}, size={len(response.content)} bytes")
        
        return response.text
        
    except requests.exceptions.Timeout as e:
        error_msg = f"Request timed out: {e}"
        log_critical_error(logger, "page fetch", TimeoutError(error_msg))
        raise requests.RequestException(error_msg)
        
    except requests.exceptions.RequestException as e:
        log_critical_error(logger, "page fetch", e)
        raise


def parse_html_content(html_content: str, logger: logging.Logger) -> BeautifulSoup:
    """Parse HTML content using BeautifulSoup.
    
    Args:
        html_content: Raw HTML content
        logger: Logger instance
        
    Returns:
        BeautifulSoup: Parsed HTML document
        
    Raises:
        ValueError: If HTML parsing fails
    """
    log_step(logger, "Parsing HTML", f"content_length={len(html_content)}")
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        log_step(logger, "HTML parsed successfully", 
                f"found {len(soup.find_all('a'))} anchor tags")
        return soup
        
    except Exception as e:
        log_critical_error(logger, "HTML parsing", e)
        raise ValueError(f"Failed to parse HTML: {e}")


def extract_anchor_elements(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """Extract all anchor elements with href attributes.
    
    Args:
        soup: Parsed HTML document
        
    Returns:
        List[Dict[str, str]]: List of anchor element data
    """
    return [
        {
            'href': link.get('href', '').strip(),
            'text': link.get_text(strip=True),
            'title': link.get('title', ''),
            'download': link.get('download', '')
        }
        for link in soup.find_all('a', href=True)
        if link.get('href', '').strip()
    ]


def matches_extension(href: str, extension: str) -> bool:
    """Check if a URL matches the target extension.
    
    Args:
        href: URL to check
        extension: Target file extension
        
    Returns:
        bool: True if URL matches extension
    """
    # Parse URL and check extension
    parsed_url = urlparse(href.lower())
    path = parsed_url.path
    extension_lower = extension.lower()
    
    # Direct path match
    if path.endswith(f'.{extension_lower}'):
        return True
    
    # Check query parameters for filename
    if '?' in href and not path.endswith(f'.{extension_lower}'):
        return f'.{extension_lower}' in href.lower()
    
    return False


def filter_links_by_extension(anchor_data: List[Dict[str, str]], 
                            extension: str, 
                            logger: logging.Logger) -> List[Dict[str, str]]:
    """Filter anchor elements by file extension.
    
    Args:
        anchor_data: List of anchor element data
        extension: Target file extension
        logger: Logger instance
        
    Returns:
        List[Dict[str, str]]: Filtered anchor data
    """
    log_step(logger, "Filtering links by extension", f"extension=.{extension}")
    
    matching_links = [
        link for link in anchor_data
        if matches_extension(link['href'], extension)
    ]
    
    log_step(logger, "Link filtering completed", 
            f"found {len(matching_links)} matching links out of {len(anchor_data)} total")
    
    # Debug log each matching link
    for link in matching_links:
        logger.debug(f"Found matching link: {link['href']}")
    
    return matching_links


def extract_filename_from_url(url: str, link_data: Dict[str, str], extension: str) -> str:
    """Extract filename from URL or link data.
    
    Args:
        url: Absolute URL
        link_data: Link metadata
        extension: File extension
        
    Returns:
        str: Extracted filename
    """
    # Try download attribute first
    if link_data.get('download'):
        return link_data['download']
    
    # Extract from URL path
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    filename = path_parts[-1] if path_parts else ''
    
    # Handle query parameters
    if '?' in filename:
        filename = filename.split('?')[0]
    
    # Fallback to generated filename
    if not filename or not filename.endswith(f'.{extension}'):
        base_url = parsed_url.netloc.replace('www.', '')
        timestamp = int(time.time())
        filename = f"{base_url}_{timestamp}.{extension}"
    
    return filename


def extract_size_hint_from_text(text: str) -> Optional[str]:
    """Extract file size hint from text.
    
    Args:
        text: Text to search for size information
        
    Returns:
        Optional[str]: Size hint if found
    """
    import re
    
    # Common size patterns: "1.5MB", "(2.3 KB)", "3.7 GB"
    size_pattern = r'[\(\[]?\s*(\d+\.?\d*\s*[KMGT]?B)\s*[\)\]]?'
    match = re.search(size_pattern, text, re.IGNORECASE)
    
    return match.group(1) if match else None


def convert_to_absolute_url(href: str, base_url: str) -> str:
    """Convert relative URL to absolute URL.
    
    Args:
        href: Relative or absolute URL
        base_url: Base URL for resolving relatives
        
    Returns:
        str: Absolute URL
        
    Raises:
        ValueError: If URL is invalid
    """
    absolute_url = urljoin(base_url, href)
    
    # Validate the URL
    parsed_url = urlparse(absolute_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError(f"Invalid URL: {absolute_url}")
    
    return absolute_url


def process_single_link(link_data: Dict[str, str], 
                       base_url: str, 
                       extension: str) -> Dict[str, Any]:
    """Process a single link into structured data.
    
    Args:
        link_data: Raw link data
        base_url: Base URL for resolving relatives
        extension: File extension
        
    Returns:
        Dict[str, Any]: Processed link data
        
    Raises:
        ValueError: If link cannot be processed
    """
    href = link_data['href']
    
    # Convert to absolute URL
    absolute_url = convert_to_absolute_url(href, base_url)
    
    # Extract filename
    filename = extract_filename_from_url(absolute_url, link_data, extension)
    
    # Get link text or use filename as fallback
    link_text = link_data['text'] or link_data['title'] or filename
    
    # Try to extract size hint
    size_hint = extract_size_hint_from_text(link_text)
    
    return {
        'url': absolute_url,
        'filename': filename,
        'text': link_text,
        'size_hint': size_hint
    }


def remove_duplicate_urls(processed_links: List[Dict[str, Any]], 
                         logger: logging.Logger) -> List[Dict[str, Any]]:
    """Remove duplicate URLs from processed links.
    
    Args:
        processed_links: List of processed link data
        logger: Logger instance
        
    Returns:
        List[Dict[str, Any]]: Links with duplicates removed
    """
    seen_urls: Set[str] = set()
    unique_links = []
    
    for link in processed_links:
        url = link['url']
        if url not in seen_urls:
            seen_urls.add(url)
            unique_links.append(link)
        else:
            logger.debug(f"Skipping duplicate URL: {url}")
    
    log_step(logger, "Duplicate removal", 
            f"removed {len(processed_links) - len(unique_links)} duplicates")
    
    return unique_links


def process_extracted_links(raw_links: List[Dict[str, str]], 
                          base_url: str, 
                          extension: str, 
                          logger: logging.Logger) -> List[Dict[str, Any]]:
    """Process raw extracted links into structured data.
    
    Args:
        raw_links: List of raw link data
        base_url: Base URL for resolving relatives
        extension: File extension
        logger: Logger instance
        
    Returns:
        List[Dict[str, Any]]: Processed and deduplicated links
    """
    log_step(logger, "Processing extracted links", f"count={len(raw_links)}")
    
    processed_links = []
    
    for link_data in raw_links:
        try:
            processed_link = process_single_link(link_data, base_url, extension)
            processed_links.append(processed_link)
            
        except Exception as e:
            logger.warning(f"Failed to process link {link_data.get('href', 'unknown')}: {e}")
            continue
    
    # Remove duplicates
    unique_links = remove_duplicate_urls(processed_links, logger)
    
    log_step(logger, "Link processing completed", 
            f"processed {len(unique_links)} unique links")
    
    return unique_links


# Composition functions for the main extraction pipeline
def extract_links_from_endpoint(config: CrawlerConfig, logger: logging.Logger) -> List[Dict[str, Any]]:
    """Main function to extract links from endpoint using functional approach.
    
    Args:
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        List[Dict[str, Any]]: List of extracted and processed links
        
    Raises:
        requests.RequestException: For network-related errors
        ValueError: For parsing errors
    """
    log_step(logger, "Starting link extraction", f"endpoint={config.endpoint}")
    
    # Create session
    session = create_session(config)
    
    try:
        # Functional pipeline using function composition
        html_content = fetch_page_content(config.endpoint, session, logger)
        soup = parse_html_content(html_content, logger)
        anchor_data = extract_anchor_elements(soup)
        matching_links = filter_links_by_extension(anchor_data, config.extension, logger)
        processed_links = process_extracted_links(matching_links, config.endpoint, config.extension, logger)
        
        logger.info(f"Successfully extracted {len(processed_links)} {config.extension} links")
        return processed_links
        
    finally:
        session.close()
        log_step(logger, "Session closed")


# Higher-order functions for advanced processing
def apply_link_filter(filter_func, links: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply a filter function to a list of links.
    
    Args:
        filter_func: Function that takes a link dict and returns bool
        links: List of link dictionaries
        
    Returns:
        List[Dict[str, Any]]: Filtered links
    """
    return [link for link in links if filter_func(link)]


def transform_links(transform_func, links: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply a transformation function to each link.
    
    Args:
        transform_func: Function that transforms a link dict
        links: List of link dictionaries
        
    Returns:
        List[Dict[str, Any]]: Transformed links
    """
    return [transform_func(link) for link in links]


def group_links_by(key_func, links: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group links by a key function.
    
    Args:
        key_func: Function that extracts grouping key from link
        links: List of link dictionaries
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Grouped links
    """
    groups = {}
    for link in links:
        key = key_func(link)
        if key not in groups:
            groups[key] = []
        groups[key].append(link)
    return groups


# Utility predicates for filtering
def has_size_hint(link: Dict[str, Any]) -> bool:
    """Check if link has size hint information."""
    return link.get('size_hint') is not None


def filename_contains(substring: str):
    """Create a predicate that checks if filename contains substring."""
    def predicate(link: Dict[str, Any]) -> bool:
        return substring.lower() in link.get('filename', '').lower()
    return predicate


def url_matches_domain(domain: str):
    """Create a predicate that checks if URL matches domain."""
    def predicate(link: Dict[str, Any]) -> bool:
        parsed_url = urlparse(link.get('url', ''))
        return domain.lower() in parsed_url.netloc.lower()
    return predicate


# Functional aggregation functions
def count_links_by_domain(links: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count links by domain.
    
    Args:
        links: List of link dictionaries
        
    Returns:
        Dict[str, int]: Domain counts
    """
    domain_counts = {}
    for link in links:
        parsed_url = urlparse(link.get('url', ''))
        domain = parsed_url.netloc
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    return domain_counts


def get_total_estimated_size(links: List[Dict[str, Any]]) -> Tuple[int, str]:
    """Calculate total estimated size from size hints.
    
    Args:
        links: List of link dictionaries
        
    Returns:
        Tuple[int, str]: (size_in_bytes, formatted_size)
    """
    import re
    
    total_bytes = 0
    
    for link in links:
        size_hint = link.get('size_hint')
        if not size_hint:
            continue
        
        # Parse size hint (e.g., "1.5MB", "500KB")
        match = re.match(r'(\d+\.?\d*)\s*([KMGT]?B)', size_hint.upper())
        if not match:
            continue
        
        size_value = float(match.group(1))
        size_unit = match.group(2)
        
        # Convert to bytes
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }
        
        if size_unit in multipliers:
            total_bytes += int(size_value * multipliers[size_unit])
    
    # Format total size
    def format_bytes(bytes_value):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f}PB"
    
    return total_bytes, format_bytes(total_bytes)


# Pipeline composition utility
def compose(*functions):
    """Compose functions from right to left."""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


# Example usage of functional composition
def create_link_processing_pipeline(config: CrawlerConfig, logger: logging.Logger):
    """Create a composable link processing pipeline.
    
    Args:
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Function: Composed pipeline function
    """
    # Define individual processing steps
    def fetch_and_parse(config):
        return extract_links_from_endpoint(config, logger)
    
    def filter_by_size(links):
        # Only keep links with size hints > 1MB (if available)
        return apply_link_filter(
            lambda link: not link.get('size_hint') or 'MB' in link.get('size_hint', ''),
            links
        )
    
    def sort_by_filename(links):
        return sorted(links, key=lambda link: link.get('filename', ''))
    
    # Compose the pipeline
    return compose(sort_by_filename, filter_by_size, fetch_and_parse)


# Main extraction function with error handling
def extract_links_safe(config: CrawlerConfig, logger: logging.Logger) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Safely extract links with comprehensive error handling.
    
    Args:
        config: Crawler configuration
        logger: Logger instance
        
    Returns:
        Tuple[List[Dict[str, Any]], Optional[str]]: (links, error_message)
    """
    try:
        links = extract_links_from_endpoint(config, logger)
        return links, None
    
    except requests.RequestException as e:
        error_msg = f"Network error during link extraction: {e}"
        log_critical_error(logger, "link extraction", e)
        return [], error_msg
    
    except ValueError as e:
        error_msg = f"Parsing error during link extraction: {e}"
        log_critical_error(logger, "link extraction", e)
        return [], error_msg
    
    except Exception as e:
        error_msg = f"Unexpected error during link extraction: {e}"
        log_critical_error(logger, "link extraction", e)
        return [], error_msg