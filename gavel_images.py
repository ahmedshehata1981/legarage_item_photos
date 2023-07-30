import streamlit as st
import webbrowser
import requests
import re
import os
import time

def extract_urls(text):
    """Extracts the URLs from the text."""
    pattern = r'"urls": "(.*?)"'
    matches = re.findall(pattern, text)
    urls = []
    for match in matches:
        urls.append(match)
    return urls



def download_image(url, filename):
    """Downloads an image from a URL and saves it to a file."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print("Error downloading image.")
        
        
        
def extract_image_name(url):
    """Extracts the image name from the URL."""
    pattern = r'/API/ShowImage/DownloadImageToServer/(.*)'
    match = re.search(pattern, url)
    if match:
        image_name = match.group(1)
    else:
        image_name = None
    return image_name

def get_links_text(code):
    """extract the text of the image urls from the api came from gavel"""
    api = 'http://41.32.175.122:3000/api/photoFBAfterEdite/'
    code_images_url = api + code
    response = requests.get(code_images_url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        text = re.findall(r'"urls": "(.*)"', content)
    else:
        return None
    return text


def download_all_images (urls):
    '''Take the list of image urls and download them in the computer'''
    if urls:
        for url in urls:
            filename = extract_image_name(url)
            download_image(url, filename)
    else:
        print("No images found.")
        
def show_images(urls):
    """Shows the images in a grid."""
    images = []
    for url in urls:
        image = st.image(url)
        images.append(image)
    return images

if __name__ == "__main__":
    st.title("Download Images from Gavel")
    code = st.text_input("Enter the code here:")
    code = code.strip()
    text = get_links_text(code)
    if st.button("Download Images"):
        download_all_images (text)
        success = st.success("Images downloaded successfully!")
        time.sleep(3)
        success.empty()
    if st.button("Show Images"):
        images = show_images(text)
