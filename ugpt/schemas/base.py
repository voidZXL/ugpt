from openai.openai_object import OpenAIObject
from utype import DataClass, dataclass


class OpenAISchema(DataClass, OpenAIObject):
    def __delitem__(self, k):
        raise NotImplementedError("del is not supported")
