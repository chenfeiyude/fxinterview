import logging
from django.contrib.sites.shortcuts import get_current_site


def format_date(date, date_format):
    date_format_str = None
    if date and date_format:
        date_format_str = date.strftime(date_format)

    return date_format_str


def format_date_b_d_y_h_m_s(date):
    return format_date(date, '%b %d, %Y %H:%M:%S')


def decode_utf_8(data):
    decoded_data = data
    if data:
        try:
            decoded_data = data.decode('utf-8')
        except UnicodeDecodeError as e:
            logging.error('Decode to utf-8 failed: %s' % e)
    return decoded_data


def get_domain_url(request):
    return ''.join(['http://', get_current_site(request).domain])
