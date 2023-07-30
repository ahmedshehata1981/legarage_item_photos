import streamlit as st
import webbrowser
import requests
# from bs4 import BeautifulSoup as bs
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
            for chunk in response.iter_content(chunk_size=1024):
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

# def get_links_text (code):
#     '''extract the text of the image urls from the api came from gavel'''
#     api = 'http://41.32.175.122:3000/api/photoFBAfterEdite/'
#     code_images_url = api + code
#     web_page = requests.get(code_images_url)
#     if web_page.status_code == 200:
#         web_page_code = bs(web_page.content,'html')
#     else:
#         return None
#     text = str(web_page_code)
#     return text

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

# def get_links_text(code):
#     """extract the text of the image urls from the api came from gavel"""
#     api = 'http://41.32.175.122:3000/api/photoFBAfterEdite/'
#     code_images_url = api + code
#     response = requests.get(code_images_url)
#     if response.status_code == 200:
#         content = response.content.decode('utf-8')
#         links = str(content).split('"')
#         urls = []
#         for link in links:
#             if link.startswith('"urls": "'):
#                 urls.append(link[10:-1])
#         text = ','.join(urls)
#     else:
#         return None
#     return text


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
    if st.button("Download Images"):
        text = get_links_text(code)
#         urls = extract_urls(text)
#         download_all_images (urls)
        download_all_images (text)
        success = st.success("Images downloaded successfully!")
        time.sleep(3)
        success.empty()
        images = show_images(text)
