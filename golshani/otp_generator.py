from django.utils.crypto import get_random_string
from random import choice
from django.conf import settings
import math
from django.core.cache import cache
from ippanel import Client
import logging
logger = logging.getLogger(__name__)




def generate_otp(k):
    rand_str = get_random_string(length=k, allowed_chars="1234567890")
    base_num = int(math.pow(10, k - 1))
    while int(rand_str) < base_num:
        number_list = [x for x in range(10)]
        num = str(choice(number_list))
        rand_str = str(int(rand_str)) + num
    return rand_str



def create_otp(user_phone, template):
    old_cache_time = cache.ttl(user_phone)
    if old_cache_time > 0:
        return False
    rand_num = generate_otp(4)
    cache.set(user_phone, rand_num, timeout=90)
    try:
        sms = Client(settings.FARAZ)
        pattern_values = {
            "token": rand_num,
            }
        sms.send_pattern(template,"+983000505", user_phone, pattern_values,)
        return True
    except Exception as e:
        logger.debug(e)
        return False



def one_token(token, user_phone, template):
    try:
        sms = Client(settings.FARAZ)
        pattern_values = {
            "token": token,
            }
        sms.send_pattern(template,"+9810001", user_phone, pattern_values,)
        return True
    except Exception as e:
        logger.debug(e)
        return False


def two_tokens(token, token2, user_phone, template):
    try:
        sms = Client(settings.FARAZ)
        pattern_values = {
            "token": token,
            'token2': token2,
            }
        sms.send_pattern(template,"+9810001", user_phone, pattern_values,)
        return True
    except Exception as e:
        logger.debug(e)
        return False
