

def fx_format_date(date, date_format):
    date_format_str = None
    if date and date_format:
        date_format_str = date.strftime(date_format)

    return date_format_str


def fx_format_date_b_d_y_h_m_s(date):
    return fx_format_date(date, '%b %d, %Y %H:%M:%S')