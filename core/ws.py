import json
from time import sleep

from asgiref.sync import sync_to_async
from channels.generic.websocket import (AsyncJsonWebsocketConsumer,
                                        JsonWebsocketConsumer, async_to_sync)

from core.utility import *
from room.models import Message, Room
from user.models import User


class GptResponseGenerator(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 파라미터 값으로 채팅 룸을 구별
        print("GPT RESPONSE CONNECT")
        # print(self.scope['headers'])
        username = self.scope['url_route']['kwargs']['username']
        try:
            user = await User.get_user(username)
        except User.DoesNotExist:
            print_colored('No User Exists!', "red")
            await self.close()
        self.user = user
        self.room_name = user.get_room_name()
        room_count = await user.get_room_count()
        self.room = await sync_to_async(Room.objects.create)(
            user=user, count=room_count)

        await self.accept()

        hello_message = f"안녕하세요! {username}님! 반가워요!"
        await self.send_output_text(hello_message)

        hello_message_audio_url = get_audio_file_url_using_polly(
            hello_message)
        await self.send_audio_url(hello_message_audio_url)
        await self.send_finish_signal()

        await sync_to_async(Message.objects.create)(
            room=self.room, audio_url=hello_message_audio_url, text=hello_message, role='assistant')

    async def disconnect(self, close_code):
        print_colored("DISCONNECT GPT RESPONSE", "yellow")

    # 웹소켓으로부터 메세지 받음

    async def receive(self, text_data):
        data = json.loads(text_data)
        audio_file = data.get('audio_file', None)
        audio_data = decode_audio(audio_file)
        input_audio_url = save_audio(audio_data, create_input_file_name())
        text_gotten_by_input_data = generate_text(audio_data)
        await self.send_input_text(text_gotten_by_input_data)
        await sync_to_async(Message.objects.create)(
            room=self.room, audio_url=input_audio_url, text=text_gotten_by_input_data, role='user')
        print_colored(
            f'RECEIVE AND SEND: {text_gotten_by_input_data}', 'green')
        # TO DO : messages by user DB (using ROOM_NAME)
        messages = await self.room.get_messages()
        messages = add_user_message_to_messages(
            messages, text_gotten_by_input_data)
        for sentence in get_sentences_by_chatgpt(messages):
            if sentence.strip() == "":
                continue
            if len(sentence) < 10:  # 숫자의 경우 너무 짧아서 에러가 남
                sleep(1)
            messages = add_assistant_message_to_messages(messages, sentence)
            output_audio_url = get_audio_file_url_using_polly(sentence)
            await self.send_output_text(sentence)
            print_colored(f'SEND OUTPUT TEXT : {sentence}', "yellow")
            await self.send_audio_url(output_audio_url)
            print_colored(f"SEND AUDIO URL : {output_audio_url}", "yellow")
            await sync_to_async(Message.objects.create)(
                room=self.room, audio_url=audio_file, text=sentence, role='assistant')

        await self.send_finish_signal()

    # 룸 그룹으로부터 메세지 받음
    async def send_input_text(self, text):
        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            "type": "input_text",
            "content": text
        }))

    async def send_output_text(self, text):
        await self.send(text_data=json.dumps({
            "type": "output_text",
            "content": text
        }))

    async def send_finish_signal(self):
        await self.send(text_data=json.dumps({
            "type": "finish_signal",
            "content": "FINISH!"
        }))

    async def send_audio_url(self, audio_url):
        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            "type": "audio_url",
            "content": audio_url
        }))


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        # 파라미터 값으로 채팅 룸을 구별
        print("CONNECT!!!")
        # print(self.scope['headers'])
        self.room_name = "DEFUALT_ROOM"
        self.room_group_name = 'chat_%s' % self.room_name

        self.accept()
        # 룸 그룹에 참가
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        print(self.channel_name)

        sleep(1)

        async_to_sync(self.channel_layer.send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': "SSIBAL!"
            }
        )

        sleep(1)

        async_to_sync(self.channel_layer.send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': "SAEGGIYA"
            }
        )

    def disconnect(self, close_code):
        print("DISCONNECT!!!")
        # 룸 그룹 나가기
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음
    def receive(self, text_data):
        print("RECEIVE!!!")
        print(text_data)
        data_json = json.loads(text_data)
        message = data_json.get('message', None)
        data = data_json.get('data', None)
        print("MESSAGE : ", message)
        print('DATA', data)
        reversing_data = message or data
        # 룸 그룹으로 메세지 보냄
        async_to_sync(self.channel_layer.send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': reversing_data[::-1]
            }
        )

    # 룸 그룹으로부터 메세지 받음
    def chat_message(self, event):
        print("CHAT_MESSAGE!!!")
        message = event['message']
        print("REVERSE_MESSAGE : ", message)

        self.send(text_data=json.dumps({
            'message': message
        }))
