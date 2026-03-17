# PDF Crawler Configuration File
# =================================

# Crawler Configuration
# ---------------------
# Target endpoint to crawl for PDF links
ENDPOINT=https://archive.org/details/kappa-magazine

# File extension to search for (without the dot)
EXTENSION=pdf

# Timeout for HTTP requests in seconds (max 3600 = 1 hour)
TIMEOUT_IN_SECONDS=300

# Downloader Configuration
# -----------------------
# Target folder for downloaded files (supports ~ for home directory)
TARGET_FOLDER=~/Downloads

# Whether to stop on first download error (true/false)
# - true: Stop immediately on first failed download
# - false: Continue downloading remaining files even if some fail
FAIL_ON_ERROR=false

# Logging Configuration
# --------------------
# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
# - DEBUG: All steps and detailed information
# - INFO: General information and progress
# - WARNING: Warning messages only
# - ERROR: Critical errors only
LOG_LEVEL=INFO

# Log file path (optional, leave empty to disable file logging)
LOG_FILE=app_crawler.log

# Configuration Examples
# =====================
# 
# Example 1: Download technical papers
# ENDPOINT=https://arxiv.org/list/cs.AI/recent
# EXTENSION=pdf
# TARGET_FOLDER=~/Documents/Papers
# 
# Example 2: Download from different domain
# ENDPOINT=https://example.com/downloads
# EXTENSION=docx
# TARGET_FOLDER=/tmp/documents
# TIMEOUT_IN_SECONDS=600
# FAIL_ON_ERROR=true
#
# Example 3: Debug mode for troubleshooting
# LOG_LEVEL=DEBUG
# LOG_FILE=/var/log/crawler_debug.log
