import pyautogui, hashlib, os, getpass,sys
from functools import wraps
from platform import system
from app.config import Config
from app.customError import NoUserName,NoGoodPassword
class Logging(object):
    def __init__(self):
        pass

    def __call__(self):
        pass

class CheckEngine(object):
    def __init__(self):
        if system().lower() == "linux":
            Config.cfg["SYSTEM"] = "linux"
            if os.environ["DISPLAY"]:
                Config.cfg["DISPLAY"] = 1
            else:
                Config.cfg["DISPLAY"] = 0
        if system().lower() == "windows":
            Config.cfg["SYSTEM"] = "windows"
            Config.cfg["DISPLAY"] = 1


class UserRequired(CheckEngine):
    def __init__(self,functie):
        super().__init__()
        self.functie = functie
    def __call__(self,text="Insert user to login with",title="CheckPoint",*args, **kwargs):

        if Config.cfg["DISPLAY"] == 0:
            self.user_request()
        if Config.cfg["DISPLAY"] == 1:
            self.mutted_user_request()


    def user_request(self):
        user_provided = pyautogui.prompt(text=text, title=title)
        try:
            if len(user_provided) > 4 and self.getUser(user_provided):
                Config.logged["tried"] = user_provided
                return self.functie()
            else:
                raise NoUserName("No user and length of it is smaller then 4")
        except TypeError:
            pass
    def mutted_user_request(self):
        print("Enter user ")
        user_provided = input()
        try:
            if len(user_provided) > 4 and self.getUser(user_provided):
                Config.logged["tried"] = user_provided
                return self.functie()
            else:
                raise NoUserName("No user and length of it is smaller then 4")
        except TypeError:
            pass

    def getUser(self,user):
        for i in Config.cfg["USER"]:
            if i["name"] == user:
                return True
        return False

class PassRequired(CheckEngine):
    def __init__(self, functie):
        super().__init__()
        self.functie = functie

    def __call__(self, *args,**kwargs):
        if Config.cfg["DISPLAY"] == 0:
            self.password_request()
        if Config.cfg["DISPLAY"] == 1:
            self.mutted_password_request()

    def password_request(self,text="Password", mask="*", title="CheckPoint"):

        passowrd_provided = pyautogui.password(text=text, mask=mask, title=title)
        secure_password = self.hash_the_passwd(passowrd_provided)
        if Config.logged["user"] == secure_password:
            return f"{secure_password} > " + str(self.functie())
        raise NoGoodPassword("Nemtodom")

    def mutted_password_request(self,text="Password", mask="*", title="CheckPoint"):
        print("adauga parola")
        passowrd_provided = getpass.getpass(prompt=text,stream=sys.stdout)
        secure_password = self.hash_the_passwd(passowrd_provided)
        if Config.logged["user"] == secure_password:
            return f"{secure_password} > " + str(self.functie())
        raise NoGoodPassword("Nemtodom")


    def hash_the_passwd(self,parola):

        hash_parola = hashlib.new("ripemd160")
        hash_parola.update(bytes(parola, encoding="ascii"))
        return str(hash_parola.hexdigest())

@UserRequired
@PassRequired
def ceva():
    return "Neata"


print(ceva())


