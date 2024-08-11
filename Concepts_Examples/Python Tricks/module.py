import time

def connect():
    print("COnnecting to Internet .....")
    time.sleep(3)
    print("You are COnnected!.")

# connect()

# To run this module, just run it "python module.py".
# however it will get called from main python file "main.py".
# When it is called from main.py we see the result twice. Why so, its because when we import a module (every time you import a module), it has to load that entire script that means it's reading every line and since at the bottom of our code (line # 8) module we catually rann a function it read that line as well and ran it as a consequence.
# So the first good habit to always have is to always check that "__name__ == '__main__" and insert what kind of functionality you want to 

