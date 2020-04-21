import pyautogui, hashlib, os
from functools import wraps
from platform import system
from app.config import Config
from app.customError import NoUserName,NoGoodPassword

class Logging(object):
    def __init__(self):
        pass

    def __call__(self):
        pass


class UserRequired(object):
    def __init__(self,functie):
        self.functie = functie
    def __call__(self,text="Insert user to login with",title="CheckPoint",*args, **kwargs):
        user_provided = pyautogui.prompt(text=text,title=title)
        if len(user_provided) > 4 and self.getUser(user_provided):
            Config.logged["tried"] = user_provided
            return self.functie()
        else:
            raise NoUserName("No user and length of it is smaller then 4")
    def getUser(self,user):
        for i in Config.cfg["USER"]:
            if i["name"] == user:
                return True
        return False

class PassRequired(object):
    def __init__(self, functie):
        self.functie = functie
    def __call__(self, text="Password", mask="*", title="CheckPoint", *args,**kwargs):
        self.check_system()
        if Config.cfg["SYSTEM"] == "windows":
            passowrd_provided = pyautogui.password(text=text, mask=mask, title=title)
            secure_password=self.hash_the_passwd(passowrd_provided)
            if Config.logged["user"] == secure_password:
                return f"{secure_password} > " + str(self.functie())
            raise NoGoodPassword("Nemtodom")

    def hash_the_passwd(self,parola):
        hash_parola = hashlib.new("ripemd160")
        hash_parola.update(bytes(parola, encoding="ascii"))
        return str(hash_parola.hexdigest())

    def check_system(self):
        if system().lower() == "linux":
            Config.cfg["SYSTEM"] = "linux"
            # we have to check linux/windows  we have tty/stty
            if os.environ["DISPLAY"]:
                Config.cfg["DISPLAY"] = 1
        else:
            Config.cfg["SYSTEM"] = "windows"

@UserRequired
@PassRequired
def ceva():
    user = None
    return "Neata"


print(ceva())


