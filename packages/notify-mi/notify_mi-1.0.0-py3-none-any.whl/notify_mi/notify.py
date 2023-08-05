from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from notify_mi.providers import PROVIDERS
from pathlib import Path
import smtplib, ssl
from notify_mi import helper

''' 
This program uses gmail to send a SMS/MMS message to a phone number
with a known service provider and optionally to an email address.
'''

def send_message(
    message,
    sender_credentials,
    phone_number = None,
    phone_provider = None, 
    subject = None, 
    send_to = None, 
    threaded = False, 
    file_attachment = None):
    
    '''
    Send a message using gmail via SMS/MMS, email, or both
    
    :param            str : message : message to be sent
    :param          tuple : sender_credentials : gmail credentials
    :param <optional> str : phone_number : phone number of reciever
    :param <optional> str : phone_provider : cell provider of reciever number
    :param <optional> str : subject : add a subject to message
    :param <optional> str : file_attachment : path to file to attach to message
    :param <optional> bool: threaded : user can decide if they want to not block main thread
    :param <optional> str : send_to : email address to send to
    '''
    
    # allow user to not block the main thread when calling
    if threaded:
        helper.threaded(__send_message_via_email(
            message, sender_credentials, phone_number, phone_provider, 
            subject, send_to, file_attachment))
    else:
        __send_message_via_email(
            message, sender_credentials, phone_number, phone_provider, 
            subject, send_to, file_attachment)


def __send_message_via_email(
    message,
    sender_credentials,
    phone_number = None,
    phone_provider = None, 
    subject = None, 
    send_to = None, 
    file_attachment = None):
    
    # ensure that credentials and info added meets specifications
    __check_for_exceptions(phone_number, phone_provider, send_to)
    
    # initialize variables needed
    _phone_number: str = phone_number
    _message: str = message
    file_attachment: str = file_attachment
    _subject: str = subject
    _phone_provider: str = phone_provider
    _sender_credentials: tuple = sender_credentials
    smtp_server: str = helper.SMTP_GMAIL
    smtp_port: int = helper.SMTP_PORT
    if file_attachment is not None:
        attachment = Path(file_attachment)
        mime_subtype: str = attachment.suffix
        mime_maintype: str = helper.find_ext_mime_type(mime_subtype)
        file_name: str = attachment.name
    
    # determine type(s) of messages being sent
    is_sending_text_message = True if None not in [_phone_number, _phone_provider] else False
    is_sending_email = True if send_to is not None and send_to is not helper.EMPTY else False
        
    # retrieve information needed to send message
    sender_email, email_password = _sender_credentials
    # get message type (sms/mms) based on provider
    # some do not have mms capabilities
    if is_sending_text_message:
        message_type = helper.MESSAGE_TYPE[0] \
            if PROVIDERS.get(_phone_provider).get(helper.MMS_SUPPORT_KEY) \
            else helper.MESSAGE_TYPE[1]
        # create receiver email based on their phone number and carrier
        receiver_phone_number = f'{_phone_number}@{PROVIDERS.get(_phone_provider).get(message_type)}'
    
    # create gmail body
    email_message = MIMEMultipart()
    if _subject is not None:
        email_message["Subject"] = _subject
    email_message["From"] = sender_email
    email_message.attach(MIMEText(_message, helper.TEXT_TYPE))
    
    # if file was included, attach to message
    if file_attachment is not None and Path(file_attachment).is_file:
        # gmail does not allow a file > 1 MB to be attached
        # therefore the entire message will not be sent
        if attachment.stat().st_size > 1 * helper.MB:
            raise helper.FileSizeExceeded
        
        # open file being sent and attach to email_message
        with open(file_attachment, helper.READ_BINARY) as attachment:
            part = MIMEBase(mime_maintype, mime_subtype)
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_name}",)
            email_message.attach(part)

    # send the message
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context = ssl.create_default_context()) as email:
        # login to gmail
        email.login(sender_email, email_password)
        
        # send SMS/MMS message
        if is_sending_text_message:
            # send email with body and attachment
            email.sendmail(sender_email, receiver_phone_number, email_message.as_string())
            
        # send to email address
        if is_sending_email:
            # send email with body and attachment
            email.sendmail(sender_email, send_to, email_message.as_string())


def __check_for_exceptions(phone_number, phone_provider, send_to): 
    # check if at least one message type is being sent
    # check if all paramters is empty
    if None in [phone_number, phone_provider]:
        # if either phone number or phone provider is not empty
        # specify that one of them is missing
        if phone_number is not None or phone_provider is not None:
            raise helper.MessageTextError
        # else, all of them is empty, thus give user a specific error message
        elif send_to is None:
            raise helper.MessageError
    elif phone_number is not None and phone_provider is not None:
        # ensure reciever email is formatted correctly
        if send_to is not None and send_to is not helper.EMPTY:
            if helper.AT_SYMBOL not in send_to or helper.EMAIL_SUFFIX not in send_to:
                raise helper.EmailFormatError
        # verify phone number is formatted correctly
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise helper.PhoneNumberError
        # verify provider given is found in providers.py
        if PROVIDERS.get(phone_provider) is None:
            raise helper.ProviderNotRecognized
        