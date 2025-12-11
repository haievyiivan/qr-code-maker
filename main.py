#
# QR Code Generator Script
#
# Note: This script requires the 'qrcode' library.
#
import qrcode
import argparse
import os
import re

class ConsoleColors:
    WARNING = "\033[93m"
    ENDC = "\033[0m"
    SUCCESS = "\033[92m"
    FAIL = "\033[91m"
    INFO = "\033[94m"

def generate_name(url):
    name = url.replace("https://", "").replace("http://", "")
    name = name.replace("/", "_")
    name = re.sub(r'[^\w\.\-]', '', name)
    return name[:30] + ".png" # truncate to 30 characters for safety

def main():
    parser = argparse.ArgumentParser(description="Generate a QR code from a URL.")
    
    parser.add_argument(
        "url", 
        nargs="?", 
        help="The URL or text to encode."
    )
    
    parser.add_argument(
        "-o", "--output", 
        default=".", 
        help="Directory to save the image."
    )
    
    parser.add_argument(
        "-n", "--name", 
        default=None, 
        help="Custom filename: make sure to add .png at the end (default: auto-generated from URL)."
    )

    args = parser.parse_args()

    url = args.url
    if not url:
        url = "https://haievyiivan.github.io"
        print(f"{ConsoleColors.WARNING}No URL provided.{ConsoleColors.ENDC} Generating default for: {url}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    if args.output != ".":
        os.makedirs(args.output, exist_ok=True)
    
    if args.name is None:
        final_name = generate_name(url)
    else:
        final_name = args.name

    full_path = os.path.join(args.output, final_name)

    try:
        img.save(full_path)
        print(f"{ConsoleColors.SUCCESS}Success!{ConsoleColors.ENDC} Saved to: {full_path}")
    except Exception as e:
        print(f"{ConsoleColors.FAIL}Error saving file:{ConsoleColors.ENDC} {e}")

if __name__ == "__main__":
    main()