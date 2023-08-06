class pyamon:
    """ 
        คลาส pyamon คือ
        ข้อมูลที่เกี่ยวของกับฉัน

        Example
        # ----------------
        mon = pyamon()
        mon.show_name() 
        mon.show_music()
        mon.about()
        mon.show_art()
        # ----------------
    """
    def __init__(self):
        self.name = "mon THJP"
        self.music = "https://youtu.be/6f5sozKp0R0"

    def show_name(self):
        print(f"สวัสดีฉันชื่อ : {self.name}")

    def show_music(self):
        print(f"เพลงที่ฉันชอบ : {self.music}")

    def about(self):
        text = """
        -----------------------
        Hi I'm newbie in python 
        -----------------------
        """
        print(text)

    def show_art(self):
        text ='''  
        ,________________________________       
        |__________,----------._ [____]  ""-,__  __...-----==="
                (_(||||||||||||)___________/   ""             |
                `----------' MonTHJP[ ))"-,                   |
                                        ""    `,  _,--...___  |
                                                `/          """
        ''' 
        print(text)

if __name__ == "__main__":
    mon = pyamon()
    mon.show_name() 
    mon.show_music()
    mon.about()
    mon.show_art()

    