"""
Object-oriented implementation of link extraction from web pages.
Extracts links matching specified file extension using BeautifulSoup.
"""

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional
import time
from dataclasses import dataclass

from config.settings import CrawlerConfig
from utils.logger import LoggedOperation, log_step, log_critical_error


@dataclass
class ExtractedLink:
    """Data class representing an extracted link."""
    url: str
    filename: str
    text: str
    size_hint: Optional[str] = None


class LinkExtractor:
    """Extracts links matching file extension from web pages."""
    
    def __init__(self, config: CrawlerConfig, logger: logging.Logger):
        """Initialize link extractor.
        
        Args:
            config: Crawler configuration
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Configure requests session with appropriate headers and timeout."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.session.timeout = self.config.timeout_in_seconds
        
        log_step(self.logger, "Session configured", 
                f"timeout={self.config.timeout_in_seconds}s, extension={self.config.extension}")
    
    def extract_links(self) -> List[ExtractedLink]:
        """Extract all links matching the configured extension.
        
        Returns:
            List[ExtractedLink]: List of extracted links
            
        Raises:
            requests.RequestException: For network-related errors
            ValueError: For parsing errors
        """
        with LoggedOperation(self.logger, f"link extraction from {self.config.endpoint}"):
            
            # Fetch the web page
            html_content = self._fetch_page()
            
            # Parse HTML and extract links
            soup = self._parse_html(html_content)
            raw_links = self._find_matching_links(soup)
            
            # Process and validate links
            processed_links = self._process_links(raw_links)
            
            self.logger.info(f"Successfully extracted {len(processed_links)} {self.config.extension} links")
            return processed_links
    
    def _fetch_page(self) -> str:
        """Fetch the target web page.
        
        Returns:
            str: HTML content of the page
            
        Raises:
            requests.RequestException: For network-related errors
        """
        log_step(self.logger, "Fetching webpage", self.config.endpoint)
        
        try:
            response = self.session.get(self.config.endpoint)
            response.raise_for_status()
            
            log_step(self.logger, "Page fetched successfully", 
                    f"status={response.status_code}, size={len(response.content)} bytes")
            
            return response.text
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timed out after {self.config.timeout_in_seconds} seconds"
            log_critical_error(self.logger, "page fetch", TimeoutError(error_msg))
            raise requests.RequestException(error_msg)
            
        except requests.exceptions.RequestException as e:
            log_critical_error(self.logger, "page fetch", e)
            raise
    
    def _parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content using BeautifulSoup.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            BeautifulSoup: Parsed HTML document
        """
        log_step(self.logger, "Parsing HTML", f"content_length={len(html_content)}")
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            log_step(self.logger, "HTML parsed successfully", 
                    f"found {len(soup.find_all('a'))} anchor tags")
            return soup
            
        except Exception as e:
            log_critical_error(self.logger, "HTML parsing", e)
            raise ValueError(f"Failed to parse HTML: {e}")
    
    def _find_matching_links(self, soup: BeautifulSoup) -> List[dict]:
        """Find all links matching the target extension.
        
        Args:
            soup: Parsed HTML document
            
        Returns:
            List[dict]: Raw link data
        """
        log_step(self.logger, "Searching for matching links", f"extension=.{self.config.extension}")
        
        matching_links = []
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href', '').strip()
            if not href:
                continue
            
            # Check if link matches our extension
            if self._is_matching_extension(href):
                link_data = {
                    'href': href,
                    'text': link.get_text(strip=True),
                    'title': link.get('title', ''),
                    'download': link.get('download', ''),
                    'element': link
                }
                matching_links.append(link_data)
                self.logger.debug(f"Found matching link: {href}")
        
        log_step(self.logger, "Link search completed", 
                f"found {len(matching_links)} matching links out of {len(all_links)} total")
        
        return matching_links
    
    def _is_matching_extension(self, href: str) -> bool:
        """Check if a URL matches the target extension.
        
        Args:
            href: URL to check
            
        Returns:
            bool: True if URL matches extension
        """
        # Parse URL and check extension
        parsed_url = urlparse(href.lower())
        path = parsed_url.path
        
        # Handle query parameters that might contain the file
        if '?' in href and not path.endswith(f'.{self.config.extension.lower()}'):
            # Sometimes the filename is in query parameters
            full_url = href.lower()
            return f'.{self.config.extension.lower()}' in full_url
        
        return path.endswith(f'.{self.config.extension.lower()}')
    
    def _process_links(self, raw_links: List[dict]) -> List[ExtractedLink]:
        """Process raw links into ExtractedLink objects.
        
        Args:
            raw_links: List of raw link dictionaries
            
        Returns:
            List[ExtractedLink]: Processed and validated links
        """
        log_step(self.logger, "Processing extracted links", f"count={len(raw_links)}")
        
        processed_links = []
        seen_urls: Set[str] = set()
        
        for link_data in raw_links:
            try:
                processed_link = self._process_single_link(link_data)
                
                # Skip duplicates
                if processed_link.url in seen_urls:
                    self.logger.debug(f"Skipping duplicate URL: {processed_link.url}")
                    continue
                
                seen_urls.add(processed_link.url)
                processed_links.append(processed_link)
                
            except Exception as e:
                self.logger.warning(f"Failed to process link {link_data.get('href', 'unknown')}: {e}")
                continue
        
        log_step(self.logger, "Link processing completed", 
                f"processed {len(processed_links)} unique links")
        
        return processed_links
    
    def _process_single_link(self, link_data: dict) -> ExtractedLink:
        """Process a single raw link into an ExtractedLink object.
        
        Args:
            link_data: Raw link dictionary
            
        Returns:
            ExtractedLink: Processed link object
            
        Raises:
            ValueError: If link cannot be processed
        """
        href = link_data['href']
        
        # Convert relative URLs to absolute
        absolute_url = urljoin(self.config.endpoint, href)
        
        # Validate the URL
        parsed_url = urlparse(absolute_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid URL: {absolute_url}")
        
        # Extract filename
        filename = self._extract_filename(parsed_url, link_data)
        
        # Get link text or use filename as fallback
        link_text = link_data['text'] or link_data['title'] or filename
        
        # Try to extract size hint from link text
        size_hint = self._extract_size_hint(link_text)
        
        return ExtractedLink(
            url=absolute_url,
            filename=filename,
            text=link_text,
            size_hint=size_hint
        )
    
    def _extract_filename(self, parsed_url, link_data: dict) -> str:
        """Extract filename from URL or link data.
        
        Args:
            parsed_url: Parsed URL object
            link_data: Raw link data
            
        Returns:
            str: Extracted filename
        """
        # Try download attribute first
        if link_data.get('download'):
            return link_data['download']
        
        # Extract from URL path
        path_parts = parsed_url.path.split('/')
        filename = path_parts[-1] if path_parts else ''
        
        # Handle query parameters
        if '?' in filename:
            filename = filename.split('?')[0]
        
        # Fallback to generated filename
        if not filename or not filename.endswith(f'.{self.config.extension}'):
            base_url = parsed_url.netloc.replace('www.', '')
            timestamp = int(time.time())
            filename = f"{base_url}_{timestamp}.{self.config.extension}"
        
        return filename
    
    def _extract_size_hint(self, text: str) -> Optional[str]:
        """Extract file size hint from link text.
        
        Args:
            text: Link text to search
            
        Returns:
            Optional[str]: Size hint if found
        """
        import re
        
        # Common size patterns: "1.5MB", "(2.3 KB)", "3.7 GB"
        size_pattern = r'[\(\[]?\s*(\d+\.?\d*\s*[KMGT]?B)\s*[\)\]]?'
        match = re.search(size_pattern, text, re.IGNORECASE)
        
        return match.group(1) if match else None
    
    def close(self):
        """Clean up resources."""
        if self.session:
            self.session.close()
            log_step(self.logger, "Session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
