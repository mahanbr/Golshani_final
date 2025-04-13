from django.utils.crypto import get_random_string
from random import choice
from django.conf import settings
import math
from django.core.cache import cache
from kavenegar import *



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
    phone = user_phone
    rand_num = generate_otp(4)
    cache.set(user_phone, rand_num, timeout=90)
    try:
        api = KavenegarAPI(settings.KAVENEGAR)
        params = {
            'receptor': phone,
            'template': template,
            'token': rand_num,
            'type': 'sms',
        }
        # print(rand_num)
        response = api.verify_lookup(params)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPException as e:
        print(e)
        return False


def one_token(token, user_phone, template):
    try:
        api = KavenegarAPI(settings.KAVENEGAR)
        params = {
            'receptor': user_phone,
            'template': template,
            'token': token,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPException as e:
        print(e)
        return False

def two_tokens(token, token2, user_phone, template):
    try:
        api = KavenegarAPI(settings.KAVENEGAR)
        params = {
            'receptor': user_phone,
            'template': template,
            'token': token,
            'token2': token2,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPException as e:
        print(e)
        return False

