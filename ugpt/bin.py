import sys
import utype
import os
from pathlib import Path
home = Path.home()
filepath = home / '.ugpt.env.json'
import json


class GPTCommand:
    API_KEY = "OPENAI_API_KEY"
    API_PROXY = "OPENAI_API_PROXY"

    def __init__(self, exe, *argv: str):
        self.exe = exe
        self.cmd = argv[0]
        self.argv = argv[1:]

        args = []
        kwargs = {}
        for arg in argv[1:]:
            arg = str(arg)
            if arg.startswith('--'):
                if '=' in arg:
                    key, val = arg.split('=')
                    kwargs[str(key).lstrip('--')] = val
                else:
                    kwargs[arg.lstrip('--')] = True
            elif arg.startswith('-'):
                kwargs[arg] = True
            else:
                args.append(arg)

        self.args = args
        self.kwargs = kwargs
        self.api_key = None

        if self.cmd.startswith('_'):
            print(f'ugpt: command {repr(self.cmd)} not found')

        try:
            self.func = getattr(self, self.cmd)
        except AttributeError:
            print(f'ugpt: command {repr(self.cmd)} not found')

    @utype.parse
    def chat(self, hint: str = utype.Param(alias_from=['--hint', '--system'], default='')):
        self._check_credentials()
        self._check_proxy()
        from .chat import start_chat
        start_chat(system_hint=hint)

    def help(self):
        pass

    @utype.parse
    def draw(self, *args: str, path: str = None):
        self._check_credentials()
        self._check_proxy()
        prompt = ' '.join([arg.strip("'").strip('"') for arg in args])
        if not prompt:
            print('info: you should specify a prompt to generate image')
            exit(0)
        from .image import uImage
        print(f'generating image for {repr(prompt)}...')
        img = uImage(prompt=prompt).create()
        print(f'image generated at: {img.data[0].url}')
        name = '-'.join(prompt.split(' ')) + '.png'
        if path:
            if os.path.isdir(path):
                path = os.path.join(path, name)
        else:
            path = os.path.join(os.getcwd(), name)
        print(f'downloading to {path}...')
        img.show(path=path or name)

    @utype.parse
    def set(self,
            key: str = utype.Param(None, title='api key'),
            proxy: str = utype.Param(None, title='request proxy url')
            ):
        if key:
            self._set_env(self.API_KEY, key)
        if proxy:
            self._set_env(self.API_PROXY, proxy)

    def env(self):
        for name in [self.API_KEY, self.API_PROXY]:
            env = self._get_env(name)
            print(f'{name} = {repr(env) if env else "<empty>"}')

    @classmethod
    def _set_env(cls, name: str, value: str):
        if not value or not name:
            return None
        value = str(value).strip("'").strip('"').strip()
        os.environ.setdefault(name, value)
        if os.name == 'posix':
            os.system(f'export {name}="{value}"')
        elif os.name == 'nt':
            os.system(f'setx {name} {value}')
        if not os.path.exists(filepath):
            env = {}
        else:
            env = json.load(open(filepath, 'r'))
        env.update({name: value})
        with open(filepath, 'w') as file:
            file.write(json.dumps(env))
        # print(f'info: {name} saved!')
        return value

    @classmethod
    def _get_env(cls, name: str):
        val = os.environ.get(name)
        if not val:
            if os.path.exists(filepath):
                env = json.load(open(filepath, 'r'))
                val = env.get(name)
                if val:
                    os.environ.setdefault(name, val)
        return val

    def _check_credentials(self):
        api_key = self._get_env(self.API_KEY)
        if api_key:
            return
        while not api_key:
            print('info: No api key provided, please enter now')
            api_key = input(f'{self.API_KEY} = ')
        self.api_key = self._set_env(self.API_KEY, self.api_key)

    def _check_proxy(self):
        proxy = self._get_env(self.API_PROXY)
        if proxy:
            import openai
            openai.proxy = {
                'http': proxy,
                'https': proxy
            }

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


def main():
    GPTCommand(*sys.argv)()
