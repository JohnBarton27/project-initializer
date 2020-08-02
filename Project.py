class Project:

    def __init__(self, pretty_name, description=""):
        self.pretty_name = pretty_name
        self.description = description

    @property
    def no_spaces_name(self):
        return self.pretty_name.lower().replace(" ", "-")
