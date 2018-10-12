def singleton(class_: type):
    class_.instance = None

    def get_instance():
        if class_.instance is None:
            class_.instance = class_()
        return class_.instance

    class_.get_instance = get_instance

    return class_
