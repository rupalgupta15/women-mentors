import os


def return_original_profile_pic(normal_img_url):
    f_name, f_ext = os.path.splitext(normal_img_url)
    f_name = f_name.replace("_normal", "")
    original_profile_img_url = f_name + f_ext
    return original_profile_img_url
