import Foundation

def _nsurl(url: str):
    if "://" in url:
        # url is a web or file URL
        url = Foundation.NSURL.URLWithString_(url)
    elif url.startswith("/"):
        # url is a file path
        url = Foundation.NSURL.fileURLWithPath_(url)
    else:
        # Try to make the URL valid
        url = "http://" + url
        url = Foundation.NSURL.URLWithString_(url)
    return url