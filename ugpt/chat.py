import utype
from utype.types import *
import openai


class Usage(utype.Schema):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatMessage(utype.Schema):
    role: Literal['system', 'user', 'assistant']
    content: str


class ChatChoice(utype.Schema):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatResult(utype.Schema):
    created: datetime
    choices: List[ChatChoice]
    usage: Usage


class ChatCompletion(utype.Schema):
    messages: List[ChatMessage]
    model: str

    def __init__(self,
                 messages: List[ChatMessage],
                 model: str = 'gpt-3.5-turbo',
                 ):
        super().__init__(locals())

    @utype.parse
    def create(self) -> ChatResult:
        return openai.ChatCompletion.create(**self)

    @utype.parse
    async def acreate(self) -> ChatResult:
        return await openai.ChatCompletion.acreate(**self)


class ChatSession:
    def __init__(self,
                 system_hint: str = None,
                 model: str = 'gpt-3.5-turbo',
                 ):
        self.system_hint = system_hint
        self.messages = []
        if system_hint:
            self.messages.append(ChatMessage(
                role='system',
                content=system_hint
            ))
        self.model = model

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def send(self, content: str) -> str:
        self.messages.append(ChatMessage(
            role='user',
            content=content
        ))
        result = ChatCompletion(
            messages=self.messages,
            model=self.model
        ).create()
        if result.choices:
            message = result.choices[0].message
            self.messages.append(message)
            return message.content
        else:
            return '<Failed to generate response>'

    def clear(self):
        self.messages = []


@utype.parse
def start_chat(model: str = 'gpt-3.5-turbo', system_hint: str = ''):
    with ChatSession(
        system_hint=system_hint.strip(),
        model=model
    ) as chat:
        print('chat started! enter your first message, [enter q to exit]')
        while True:
            try:
                user_input = input('>>> ')
                if user_input.strip().lower() == 'q':
                    exit(0)
                message = chat.send(user_input)
                for line in message.split('. '):
                    print(line)
            except KeyboardInterrupt:
                print('chat exit')
                exit(0)
