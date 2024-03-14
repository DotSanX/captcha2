import hashlib
import random
import string
import datetime
from gtts import gTTS
from captcha.image import ImageCaptcha
import os 


def generate_captcha():
    letters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choice(letters) for i in range(6))
    image = ImageCaptcha(width=280, height=90)
    image.write(captcha_text, 'captcha.png')
    return captcha_text

def generate_audio_captcha(text):
  tts = gTTS(text=text, lang='en')
  tts.save("captcha.mp3")
  # os.system("mpg321 captcha.mp3")

def hash_with_salt(text, salt):
    return hashlib.sha256((salt + text).encode()).hexdigest()

def log_attempt(attempt_time, success):
    with open("captcha_attempts.log", "a") as log_file:
        log_file.write(f"{attempt_time} - {'Success' if success else 'Failure'}\n")

def main():
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        captcha_text = generate_captcha()
        salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        hashed_captcha = hash_with_salt(captcha_text, salt)

        print("\nNew CAPTCHA Generated.")
        captcha_type = input("Type 'audio' for audio CAPTCHA or 'text' for image CAPTCHA: ")
        if captcha_type.lower() == 'audio':
          generate_audio_captcha(captcha_text)
        elif captcha_type.lower() == 'text':
          print("Please view the CAPTCHA image in 'captcha.png' and enter the text below.")
        else:
          print("Invalid input. Please enter 'audio' or 'text'.")
          continue
        user_input = input("Enter CAPTCHA Text: ")

        current_time = datetime.datetime.now()
        if hash_with_salt(user_input, salt) == hashed_captcha:
            print("\n✅ CAPTCHA Verification Successful!")
            log_attempt(current_time, True)
            break
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            print("\n❌ Incorrect CAPTCHA.")
            log_attempt(current_time, False)
            if remaining_attempts > 0:
                print(f"You have {remaining_attempts} {'attempt' if remaining_attempts == 1 else 'attempts'} remaining.")
            else:
                print("⚠️ Maximum attempts exceeded. Please try again later.")
                break

if __name__ == "__main__":
    main()
