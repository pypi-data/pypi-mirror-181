import threading
import functools

'''
This is a helper class that contains constants 
and methods used throughout multiple files.
'''

# constants
EMPTY = ""
SMTP_GMAIL = "smtp.gmail.com"
SMTP_PORT = 465
MESSAGE_TYPE = ["mms", "sms"]
MMS_SUPPORT_KEY = "mms_support"
TEXT_TYPE = "plain"
READ_BINARY = 'rb'
AT_SYMBOL = "@"
EMAIL_SUFFIX = ".com"
MB = 1000000

# exceptions
class FileSizeExceeded(Exception):
    def __str__(self):
        return "Attachment cannot be more than 1MB."

class PhoneNumberError(Exception):
    def __str__(self):
        return "Phone number should have 10 numbers only."
    
class ProviderNotRecognized(Exception):
    def __str__(self):
        return "Select a phone provider from providers.py file."

class ExtensionNotFound(Exception):
    def __str__(self):
        return "Attached file has an extension that is not recognized."
    
class EmailFormatError(Exception):
    def __str__(self):
        return "The receiver email should follow format -> name@email.com."

class MessageError(Exception):
    def __str__(self):
        return "Message type not specified. Pick text, email, or both and include the respective paramters."

class MessageTextError(Exception):
    def __str__(self):
        return "Phone number AND phone provider required for sending a text message."

class MessageEmailError(Exception):
    def __str__(self):
        return "Receiver's email is required to send a message."

# decorator to automatically launch a function in a thread
def threaded(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

extensions_and_mime_types = [
    (".aac", "audio/aac"),    
    (".abw", "application/x-abiword"),    
    (".arc", "application/x-freearc"),    
    (".avif", "image/avif"),    
    (".avi", "video/x-msvideo"),    
    (".azw", "application/vnd.amazon.ebook"),    
    (".bin", "application/octet-stream"),    
    (".bmp", "image/bmp"),    
    (".bz", "application/x-bzip"),    
    (".bz2", "application/x-bzip2"),    
    (".cda", "application/x-cdf"),    
    (".csh", "application/x-csh"),    
    (".css", "text/css"),    
    (".csv", "text/csv"),    
    (".doc", "application/msword"),    
    (".docx", "application/vnd.openxmlformats-"),
    (".eot", "application/vnd.ms-fontobject"),    
    (".epub", "application/epub+zip"),    
    (".gz", "application/gzip"),    
    (".gif", "image/gif"),    
    (".htm, .html", "text/html"),    
    (".ico", "image/vnd.microsoft.icon"),    
    (".ics", "text/calendar"),    
    (".jar", "application/java-archive"),    
    (".jpeg, .jpg", "image/jpeg"),    
    (".js", "text/javascript"),    
    (".json", "application/json"),    
    (".jsonld", "application/ld+json"),    
    (".mid, .midi", "audio/midi, audio/x-midi"),    
    (".mjs", "text/javascript"),    
    (".mp3", "audio/mpeg"),    
    (".mp4", "video/mp4"),    
    (".mpeg", "video/mpeg"),
    (".mpkg", "application/vnd.apple.installer+xml"),    
    (".odp", "application/vnd.oasis.opendocument.presentation"),    
    (".ods", "application/vnd.oasis.opendocument.spreadsheet"),    
    (".odt", "application/vnd.oasis.opendocument.text"),    
    (".oga", "audio/ogg"),    (".ogv", "video/ogg"),    
    (".ogx", "application/ogg"),    (".opus", "audio/opus"),   
    (".otf", "font/otf"),    
    (".png", "image/png"),    
    (".pdf", "application/pdf"),   
    (".php", "application/x-httpd-php"),    
    (".ppt", "application/vnd.ms-powerpoint"),    
    (".pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),   
    (".rar", "application/vnd.rar"), 
    (".rtf", "application/rtf"),    
    (".sh", "application/x-sh"),
    (".svg", "image/svg+xml"),    
    (".tar", "application/x-tar"),    
    (".tif, .tiff", "image/tiff"),    
    (".ts", "video/mp2t"),
    (".ttf", "font/ttf"),    
    (".txt", "text/plain"),    
    (".vsd", "application/vnd.visio"),    
    (".wav", "audio/wav"),    
    (".weba", "audio/webm"),    
    (".webm", "video/webm"),    
    (".webp", "image/webp"),    
    (".woff", "font/woff"),    
    (".woff2", "font/woff2"),    
    (".xhtml", "application/xhtml+xml"),    
    (".xls", "application/vnd.ms-excel"),    
    (".xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),    
    (".xml", "application/xml"),    
    (".xul", "application/vnd.mozilla.xul+xml"),    
    (".zip", "application/zip"),    
    (".3gp", "video/3gpp"),    
    (".3g2", "video/3gpp2"),    
    (".7z", "application/x-7z-compressed")]

# param: find_ext -> desired extension to find 
# return: mime type for the desired extension
def find_ext_mime_type(find_ext):
    for extension_and_mime_type in extensions_and_mime_types:
        extension = extension_and_mime_type[0]
        if find_ext == extension:
            return extension_and_mime_type[1].split("/")[0]
    raise ExtensionNotFound
