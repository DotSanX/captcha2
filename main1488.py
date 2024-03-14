import hashlib
import random
import string
from captcha.image import ImageCaptcha
def generate_captcha():
    letters = string.ascii_uppercase + string.digits
    captcha_text = "".join(random.choice(letters) for i in range(6))
    image = ImageCaptcha(width=280, height=80)
    data = image.generate(captcha_text)

    image.write(captcha_text, "captcha.png")
    return captcha_text

def hash_with_salt(text, salt):

    return hashlib.sha256((text + salt).encode()).hexdigest()

def main():
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        captcha = generate_captcha()
        salt = ''.join(random.choice(string.ascii_uppercase + string.digits))
        hased_captcha = hash_with_salt(captcha, salt)

        print("Captcha image is generates as CAPTCH.png. Please enter it")
        user_input = input("Enter CAPTCHA: ")
        if hash_with_salt(user_input, salt) == hased_captcha:
            print("Captcha is correct")
            break
        else:
            print("Captcha is incorrect")
            attempts += 1
            if attempts < max_attempts:
                print(f"Attempts left: {max_attempts - attempts}")
            else:
                print("Captcha is expired. Please try again later")
if __name__ == "__main__":
    main()
