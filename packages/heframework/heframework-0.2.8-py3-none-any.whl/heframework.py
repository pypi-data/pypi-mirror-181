# heStudio Framework

## show框架

def show(message="请传入文本", title=None):
    import src.show
    src.show.show(message, title).show()

## list框架

def list(json_file=None, info=None):
    import src.list
    src.list.list(json_file, info).list()