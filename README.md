# Image Steganography Application

This is a Python application for performing image steganography, utilizing Least Significant Bit (LSB) steganography technique to encode and decode text messages within images. The application provides a user-friendly interface built using the Tkinter library.

## Features

- **Encode Text into Image:** Allows users to select an image file and enter a text message to hide within the image.
- **Decode Text from Image:** Enables users to select an encoded image and extract the hidden text message.
- **Copy Text to Clipboard:** Provides an option to copy the extracted text message to the clipboard for easy sharing.


## Installation

To use the Image Steganography App, follow these steps:

# 1. Clone the repository:

git clone https://github.com/SPARSH511/image-steganography-app.git

# 2. Install the required dependencies:
pip install -r requirements.txt

# 3. Run the application:
python image_steganography_app.py


## Usage
**Select Image:** Click the "Select Image" button to choose an image file for encoding or decoding.

**Encode:** Click the "Encode" button to hide a text message within the selected image. Enter the desired text message and click "Encode Text".

**Decode:** Click the "Decode" button to extract a hidden text message from an encoded image.

**Copy Text:** After decoding, click the "Copy Text" button to copy the extracted text to the clipboard.
