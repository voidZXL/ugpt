import utype
from utype.types import *
import os
import urllib.request
import PIL.Image
from openai import Image


class UrlObject(utype.Schema):
    url: str


class ImageResult(utype.Schema):
    created: datetime
    data: List[UrlObject]

    def show(self, path: str = None):
        if not self.data:
            raise ValueError('No data to show')
        name = path or 'tmp.png'
        urllib.request.urlretrieve(self.data[0].url, filename=name)
        img = PIL.Image.open(name)
        img.show()


class uImage(utype.Schema):
    prompt: str
    n: int
    size: str
    response_format: str
    user: Optional[str] = utype.Field(no_output=lambda v: v is None)

    def __init__(
        self,
        prompt: str,
        n: int = utype.Param(
            1,
            description='The number of images to generate. Must be between 1 and 10.',
        ),
        size: Literal['256x256', '512x512', '1024x1024'] = utype.Param(
            '1024x1024',
            description='The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.'
        ),
        response_format: Literal['url', 'b64_json'] = utype.Param(
            'url',
            description='The format in which the generated images are returned. Must be one of url or b64_json.'
        ),
        user: str = utype.Param(
            None,
            description='A unique identifier representing your end-user, '
                        'which can help OpenAI to monitor and detect abuse'
        )
    ):
        super().__init__(locals())

    @utype.parse
    def create(self) -> ImageResult:
        return Image.create(**self)

    @utype.parse
    async def acreate(self) -> ImageResult:
        return await Image.acreate(**self)


if __name__ == '__main__':
    img = uImage(prompt='an indie rock star on stage with his band').create()
    img.show()
