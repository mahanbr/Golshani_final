import requests
from django.conf import settings
import jdatetime
from PIL import Image
from django.core.exceptions import ValidationError



def google_recaptcha(recaptcha_response):
    data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
    r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
    )
    result = r.json()
    if result["success"]:
        return True
    return False



def format_date(user_input):
    if type(user_input) != str or 10 < len(user_input) or len(user_input) <= 7:
        return None
    try:
        ui = user_input.split('/')
        year = ui[0]
        print(year)
        month = ui[1]
        print(month)
        day = ui[2]
        print(day)
        formatted_date = jdatetime.date(
            int(year), int(month), int(day)).togregorian()
        print(formatted_date)
        return formatted_date
    except Exception as e:
        return False




def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.get_full_name(), filename)

def validate_image_file(image):
    max_size = 1 * 1024 * 1024  # 1Gb Limit
    valid_formats = ['JPEG', 'PNG', 'JPG']
    if image.size > max_size:
        raise ValidationError(f"Image size should not exceed {max_size / (1024 * 1024)} MB.")
    # Check file format
    try:
        img = Image.open(image)
        if img.format not in valid_formats:
            raise ValidationError(f"Only {', '.join(valid_formats)} formats are allowed.")
        img.verify()
    except Exception:
        raise ValidationError("Invalid image file.")
    


    
