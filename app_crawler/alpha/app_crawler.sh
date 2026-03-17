#!/bin/bash

# target URL
page_url="https://archive.org/details/kappa-magazine"
log_file="wget_kappa_magazine.log"

# get pdf links
urls=$(wget -qO- "$page_url" | grep -oP 'href="\K[^"]+\.pdf')

download_pdf() {
    url=$1
    output_file=$(basename "$url")

    echo "Downloading: $url"
    wget -c "$url" -O "$output_file" 2>> "$log_file"

    if [ $? -eq 0 ]; then
        echo "Download completed: $output_file"
    else
        echo "Error download file: $output_file." | tee -a "$log_file"
    fi
}

for url in $urls; do
    if [[ "$url" != http* ]]; then
        url="https://archive.org$url"
    fi
    download_pdf "$url"
done

echo "Download completed"
