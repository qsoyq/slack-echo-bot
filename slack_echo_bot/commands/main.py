

import typer
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_echo_bot.commands import default_invoke_without_command

helptext = """

"""

cmd = typer.Typer(help=helptext)


def add_default_invoke():
    for _cmd in (cmd,):
        _cmd.callback(invoke_without_command=True)(default_invoke_without_command)


add_default_invoke()

@cmd.command('echo-bot')
def echo_bot(slack_bot_token: str = typer.Option(..., envvar='SLACK_BOT_TOKEN'), slack_app_token: str = typer.Option(..., envvar='SLACK_APP_TOKEN')):
    app = App(token=slack_bot_token)
    app.command('/echo')(handle_echo_command)

    handler = SocketModeHandler(app, slack_app_token)
    handler.start()


def handle_echo_command(ack, body, respond):
    """
    用户在 Slack 输入:
        /echo hello world
    Slack 发送一个 command 事件到 Socket Mode，
    这里的 body["text"] 就是 "hello world"
    """
    ack()

    user_id = body['user_id']
    text = body.get('text', '').strip()

    if not text:
        respond(
            response_type='ephemeral',   # 只对发命令的人可见
            text='用法：`/echo 内容`，例如 `/echo hello`'
        )
        return

    respond(
        response_type='in_channel',     # 频道里所有人可见
        text=f'<@{user_id}> 说：{text}'
    )



if __name__ == '__main__':
    cmd()
