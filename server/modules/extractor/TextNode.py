class TextNode:

    def __init__(self, text, parent_tags, label):
        super().__init__()
        self.__text = text
        self.__parent_tags = parent_tags

        self.__parent_tag_path = ''
        for i in range(len(parent_tags)):
            tag = parent_tags[i]
            self.__parent_tag_path += tag + ('' if i == (len(parent_tags) - 1) else '/')

        self.__label = label

    def get_text(self):
        return self.__text

    def get_parent_tag_path(self):
        return self.__parent_tag_path