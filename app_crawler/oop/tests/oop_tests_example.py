"""
Comprehensive test suite for OOP PDF crawler implementation.
Covers unit tests, integration tests, and error scenarios.
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import logging
import requests

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import CrawlerConfig, ConfigManager
from oop.app_crawler_oop import PDFCrawler
from oop.app_get_links_oop import LinkExtractor, ExtractedLink
from oop.app_wget_links_oop import FileDownloader, DownloadResult


class TestCrawlerConfig:
    """Test configuration management."""
    
    def test_valid_config_creation(self):
        """Test creating valid configuration."""
        config = CrawlerConfig(
            endpoint="https://example.com/test",
            extension="pdf",
            timeout_in_seconds=300,
            target_folder="/tmp/test",
            fail_on_error=False,
            log_level="INFO",
            log_file="test.log"
        )
        
        assert config.endpoint == "https://example.com/test"
        assert config.extension == "pdf"
        assert config.timeout_in_seconds == 300
    
    def test_invalid_endpoint_raises_error(self):
        """Test that invalid endpoint raises ValueError."""
        with pytest.raises(ValueError, match="Invalid ENDPOINT URL format"):
            CrawlerConfig(
                endpoint="not-a-url",
                extension="pdf",
                timeout_in_seconds=300,
                target_folder="/tmp/test",
                fail_on_error=False,
                log_level="INFO",
                log_file="test.log"
            )
    
    def test_negative_timeout_raises_error(self):
        """Test that negative timeout raises ValueError."""
        with pytest.raises(ValueError, match="TIMEOUT_IN_SECONDS must be positive"):
            CrawlerConfig(
                endpoint="https://example.com",
                extension="pdf",
                timeout_in_seconds=-10,
                target_folder="/tmp/test",
                fail_on_error=False,
                log_level="INFO",
                log_file="test.log"
            )
    
    def test_invalid_log_level_raises_error(self):
        """Test that invalid log level raises ValueError."""
        with pytest.raises(ValueError, match="LOG_LEVEL must be one of"):
            CrawlerConfig(
                endpoint="https://example.com",
                extension="pdf",
                timeout_in_seconds=300,
                target_folder="/tmp/test",
                fail_on_error=False,
                log_level="INVALID",
                log_file="test.log"
            )


class TestLinkExtractor:
    """Test link extraction functionality."""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration for testing."""
        return CrawlerConfig(
            endpoint="https://test.com/page",
            extension="pdf",
            timeout_in_seconds=300,
            target_folder="/tmp/test",
            fail_on_error=False,
            log_level="DEBUG",
            log_file=""
        )
    
    @pytest.fixture
    def mock_logger(self):
        """Create mock logger for testing."""
        return Mock(spec=logging.Logger)
    
    @pytest.fixture
    def sample_html(self):
        """Sample HTML content with PDF links."""
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Documents</h1>
            <a href="document1.pdf">First PDF Document</a>
            <a href="/path/to/document2.pdf" title="Second Document">Document 2</a>
            <a href="https://example.com/paper.pdf">Research Paper (1.5MB)</a>
            <a href="not-a-pdf.txt">Text File</a>
            <a href="relative/document3.pdf" download="manual.pdf">Manual</a>
            <a href="duplicate.pdf">Duplicate</a>
            <a href="duplicate.pdf">Duplicate Again</a>
        </body>
        </html>
        """
    
    def test_session_setup(self, mock_config, mock_logger):
        """Test session configuration."""
        extractor = LinkExtractor(mock_config, mock_logger)
        
        assert extractor.session.timeout == 300
        assert 'Mozilla/5.0' in extractor.session.headers['User-Agent']
        
        extractor.close()
    
    @patch('oop.app_get_links_oop.requests.Session.get')
    def test_fetch_page_success(self, mock_get, mock_config, mock_logger, sample_html):
        """Test successful page fetching."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = sample_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        extractor = LinkExtractor(mock_config, mock_logger)
        
        result = extractor._fetch_page()
        
        assert result == sample_html
        mock_get.assert_called_once()
        extractor.close()
    
    @patch('oop.app_get_links_oop.requests.Session.get')
    def test_fetch_page_timeout(self, mock_get, mock_config, mock_logger):
        """Test page fetch timeout handling."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        extractor = LinkExtractor(mock_config, mock_logger)
        
        with pytest.raises(requests.RequestException, match="Request timed out"):
            extractor._fetch_page()
        
        extractor.close()
    
    def test_html_parsing(self, mock_config, mock_logger, sample_html):
        """Test HTML parsing with BeautifulSoup."""
        extractor = LinkExtractor(mock_config, mock_logger)
        
        soup = extractor._parse_html(sample_html)
        
        # Check that we can find anchor tags
        anchors = soup.find_all('a')
        assert len(anchors) == 7
        
        extractor.close()
    
    def test_extension_matching(self, mock_config, mock_logger):
        """Test file extension matching logic."""
        extractor = LinkExtractor(mock_config, mock_logger)
        
        # Test various URL formats
        assert extractor._is_matching_extension("document.pdf") is True
        assert extractor._is_matching_extension("path/to/file.PDF") is True
        assert extractor._is_matching_extension("file.pdf?version=1") is True
        assert extractor._is_matching_extension("file.txt") is False
        assert extractor._is_matching_extension("download.php?file=doc.pdf") is True
        
        extractor.close()
    
    @patch('oop.app_get_links_oop.requests.Session.get')
    def test_full_extraction_process(self, mock_get, mock_config, mock_logger, sample_html):
        """Test complete link extraction process."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = sample_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        extractor = LinkExtractor(mock_config, mock_logger)
        
        links = extractor.extract_links()
        
        # Should find 5 PDF links (excluding text file and removing duplicate)
        assert len(links) == 5
        
        # Check link structure
        for link in links:
            assert isinstance(link, ExtractedLink)
            assert link.url.startswith('http')
            assert link.filename.endswith('.pdf')
        
        # Check specific links
        filenames = [link.filename for link in links]
        assert 'document1.pdf' in filenames
        assert 'document2.pdf' in filenames
        assert 'paper.pdf' in filenames
        
        extractor.close()


class TestFileDownloader:
    """Test file download functionality."""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield CrawlerConfig(
                endpoint="https://test.com",
                extension="pdf",
                timeout_in_seconds=300,
                target_folder=temp_dir,
                fail_on_error=False,
                log_level="DEBUG",
                log_file=""
            )
    
    @pytest.fixture
    def mock_logger(self):
        """Create mock logger for testing."""
        return Mock(spec=logging.Logger)
    
    @pytest.fixture
    def sample_links(self):
        """Sample links for testing."""
        return [
            ExtractedLink(
                url="https://example.com/doc1.pdf",
                filename="document1.pdf",
                text="First Document"
            ),
            ExtractedLink(
                url="https://example.com/doc2.pdf",
                filename="document2.pdf",
                text="Second Document"
            )
        ]
    
    def test_wget_availability_check(self, mock_config, mock_logger):
        """Test wget dependency validation."""
        with patch('shutil.which', return_value=None):
            with pytest.raises(ValueError, match="wget command not found"):
                FileDownloader(mock_config, mock_logger)
    
    def test_wget_command_building(self, mock_config, mock_logger):
        """Test wget command construction."""
        with patch('shutil.which', return_value='/usr/bin/wget'):
            downloader = FileDownloader(mock_config, mock_logger)
            
            link = ExtractedLink(
                url="https://example.com/test.pdf",
                filename="test.pdf",
                text="Test PDF"
            )
            
            target_path = os.path.join(mock_config.target_folder, "test.pdf")
            cmd = downloader._build_wget_command(link, target_path)
            
            assert 'wget' in cmd
            assert str(mock_config.timeout_in_seconds) in cmd
            assert target_path in cmd
            assert link.url in cmd
    
    @patch('shutil.which', return_value='/usr/bin/wget')
    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_successful_download(self, mock_getsize, mock_exists, mock_subprocess, mock_config, mock_logger):
        """Test successful file download."""
        # Setup mocks
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Download completed"
        mock_subprocess.return_value.stderr = ""
        mock_exists.return_value = True
        mock_getsize.return_value = 1024000  # 1MB
        
        downloader = FileDownloader(mock_config, mock_logger)
        
        link = ExtractedLink(
            url="https://example.com/test.pdf",
            filename="test.pdf",
            text="Test PDF"
        )
        
        result = downloader._download_single_file(link)
        
        assert result.success is True
        assert result.filename == "test.pdf"
        assert result.file_size == 1024000
        assert result.wget_exit_code == 0
    
    @patch('shutil.which', return_value='/usr/bin/wget')
    @patch('subprocess.run')
    def test_failed_download(self, mock_subprocess, mock_config, mock_logger):
        """Test failed file download handling."""
        # Setup mocks for failed download
        mock_subprocess.return_value.returncode = 4  # Network failure
        mock_subprocess.return_value.stdout = ""
        mock_subprocess.return_value.stderr = "Network unreachable"
        
        downloader = FileDownloader(mock_config, mock_logger)
        
        link = ExtractedLink(
            url="https://example.com/nonexistent.pdf",
            filename="nonexistent.pdf",
            text="Non-existent PDF"
        )
        
        result = downloader._download_single_file(link)
        
        assert result.success is False
        assert result.wget_exit_code == 4
        assert "Network failure" in result.error_message
    
    @patch('shutil.which', return_value='/usr/bin/wget')
    @patch('oop.app_wget_links_oop.FileDownloader._download_single_file')
    def test_batch_download_with_fail_on_error(self, mock_download, mock_config, mock_logger, sample_links):
        """Test batch download with fail_on_error enabled."""
        # Configure to fail on error
        mock_config.fail_on_error = True
        
        # First download succeeds, second fails
        mock_download.side_effect = [
            DownloadResult(
                url=sample_links[0].url,
                filename=sample_links[0].filename,
                success=True,
                file_size=1000,
                download_time=1.0
            ),
            DownloadResult(
                url=sample_links[1].url,
                filename=sample_links[1].filename,
                success=False,
                error_message="Network error",
                download_time=0.5
            )
        ]
        
        downloader = FileDownloader(mock_config, mock_logger)
        result = downloader.download_files(sample_links)
        
        # Should stop after first failure
        assert result['successful_downloads'] == 1
        assert result['failed_downloads'] == 1
        assert mock_download.call_count == 2


class TestPDFCrawlerIntegration:
    """Integration tests for complete PDF crawler."""
    
    @pytest.fixture
    def temp_env_file(self):
        """Create temporary .env file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""
ENDPOINT=https://test.example.com
EXTENSION=pdf
TIMEOUT_IN_SECONDS=30
TARGET_FOLDER=/tmp/test_downloads
FAIL_ON_ERROR=false
LOG_LEVEL=DEBUG
LOG_FILE=test_crawler.log
""")
            yield f.name
        
        # Cleanup
        os.unlink(f.name)
    
    def test_crawler_initialization(self, temp_env_file):
        """Test crawler initialization with config file."""
        crawler = PDFCrawler(temp_env_file)
        
        # Should initialize without errors
        crawler.initialize()
        
        assert crawler.config is not None
        assert crawler.logger is not None
        assert crawler.link_extractor is not None
        assert crawler.file_downloader is not None
        
        # Cleanup
        crawler.cleanup()
    
    def test_missing_env_file(self):
        """Test handling of missing .env file."""
        crawler = PDFCrawler('nonexistent.env')
        
        with pytest.raises(FileNotFoundError):
            crawler.initialize()
    
    @patch('oop.app_get_links_oop.LinkExtractor.extract_links')
    @patch('oop.app_wget_links_oop.FileDownloader.download_files')
    def test_full_workflow_success(self, mock_download, mock_extract, temp_env_file):
        """Test complete successful workflow."""
        # Setup mocks
        mock_links = [
            ExtractedLink("https://example.com/doc.pdf", "doc.pdf", "Test Doc")
        ]
        mock_extract.return_value = mock_links
        
        mock_download.return_value = {
            'status': 'completed',
            'successful_downloads': 1,
            'failed_downloads': 0,
            'total_size_mb': 1.5,
            'downloaded_files': [{'filename': 'doc.pdf'}],
            'failed_files': []
        }
        
        crawler = PDFCrawler(temp_env_file)
        crawler.initialize()
        
        results = crawler.crawl_and_download()
        
        assert results['summary']['operation_status'] == 'success'
        assert results['summary']['files_downloaded'] == 1
        assert results['extraction_results']['links_found'] == 1
        
        crawler.cleanup()


class TestErrorScenarios:
    """Test various error scenarios and edge cases."""
    
    def test_network_timeout_handling(self):
        """Test network timeout handling."""
        # This would require more complex mocking of network conditions
        pass
    
    def test_malformed_html_handling(self):
        """Test handling of malformed HTML."""
        pass
    
    def test_permission_denied_download(self):
        """Test handling of permission denied during download."""
        pass
    
    def