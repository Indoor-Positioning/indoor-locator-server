from channels import Group


def ws_receive(message):
    message.reply_channel.send({
        "text": message.content['text'],
    })
