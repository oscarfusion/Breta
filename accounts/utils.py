def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def filter_user_data(data):
    if not data.get('is_current_user', False):
        if 'email' in data:
            data['email'] = None
        if 'paypal_email' in data:
            data['paypal_email'] = None
    return data
