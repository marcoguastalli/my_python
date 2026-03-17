"""
Web Crawler Package

A comprehensive web crawling package with OOP design patterns.
Includes file downloading, link extraction, and main crawling functionality.
"""

__version__ = "1.0.0"
__author__ = "marcoguastalli"

# Import main configuration
try:
    from config.settings import CrawlerConfig
except ImportError as e:
    print(f"Warning: Could not import CrawlerConfig: {e}")
    CrawlerConfig = None

# Import OOP components
try:
    from oop.oop_file_downloader import FileDownloader
except ImportError as e:
    print(f"Warning: Could not import FileDownloader: {e}")
    FileDownloader = None

try:
    from oop.oop_link_extractor import LinkExtractor, ExtractedLink
except ImportError as e:
    print(f"Warning: Could not import LinkExtractor components: {e}")
    LinkExtractor = None
    ExtractedLink = None

try:
    from oop.oop_main_crawler import MainCrawler
except ImportError as e:
    print(f"Warning: Could not import MainCrawler: {e}")
    MainCrawler = None

# Import logger utilities
try:
    from utils.logger import (
        LoggedOperation,
        log_step,
        log_download_result,
        log_progress,
        log_critical_error
    )
except ImportError as e:
    print(f"Warning: Could not import logger utilities: {e}")
    LoggedOperation = None
    log_step = None
    log_download_result = None
    log_progress = None
    log_critical_error = None

# Define what gets imported when someone does "from your_package import *"
__all__ = [
    'CrawlerConfig',
    'FileDownloader',
    'LinkExtractor',
    'ExtractedLink',
    'MainCrawler',
    'LoggedOperation',
    'log_step',
    'log_download_result',
    'log_progress',
    'log_critical_error',
]


# Package-level initialization
def get_version():
    """Return the package version."""
    return __version__


def get_available_components():
    """Return a list of successfully imported components."""
    components = []
    for component in __all__:
        if globals().get(component) is not None:
            components.append(component)
    return components


# Optional: Package-level configuration
DEFAULT_CONFIG = {
    'debug': False,
    'max_retries': 3,
    'timeout': 30,
}


# You can also add package-level functions
def quick_crawl(url, **kwargs):
    """
    Quick crawl function for simple use cases.

    Args:
        url (str): URL to crawl
        **kwargs: Additional configuration options

    Returns:
        Results from the crawler
    """
    if MainCrawler is None:
        raise ImportError("MainCrawler could not be imported")

    crawler = MainCrawler(**kwargs)
    return crawler.crawl(url)


# Print package info when imported (optional, remove if you don't want this)
print(f"Web Crawler Package v{__version__} initialized")
available = get_available_components()
print(f"Available components: {', '.join(available)}")