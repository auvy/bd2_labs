import enum
from random import randint, choice


class Tag(enum.Enum):
    family = (1, "Family")
    private = (2, "Private")
    work = (3, "Work")
    group = (4, "Group")
    news = (5, "News")
    public = (6, "Public")

    # @classmethod
    def get_member(data):
        return data in Tag._member_names_

    # @classmethod
    def get_random():
        tags = []
        num = randint(0, len(Tag))
        for i in range(num):
            tag = choice(list(Tag)).name
            if tag not in tags:
                tags.append(tag)
        return tags