class ComponentList:
    def __init__(self):
        pass

    def add(self, json_item):
        raise NotImplementedError("ComponentList: add not implemented")

    def get(self, label):
        return None

    def get_includes(self):
        return ""

    def get_pins(self):
        return ""

    def get_constructors(self):
        return ""

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return ""

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        raise NotImplementedError("ComponentList: get_indices not implemented")
