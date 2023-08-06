# heStudio Framework Show

import tkinter

class show:
    def __init__(self, message, title):
        self.code = None
        if not message:
            self.code = 25000
            self.error = 25001
        else:
            self.message = message
        if not title:
            pass
        else:
            self.title = title
    
    def show(self):
        if self.code == 25000:
            # # 该代码仅供测试使用
            # print(self.error)
            return self.error
        else:
            main = tkinter.Tk()
            if not self.title == None:
                main.title(self.title)
            else:
                pass
            message_show = tkinter.Label(main, text=self.message)
            message_show.pack(side="top")
            air = tkinter.Label(main, text=" ")
            air.pack(side="top")
            ok = tkinter.Button(main, text="确定", command=main.destroy)
            ok.pack(side="bottom")
            main.mainloop()
            return 20000