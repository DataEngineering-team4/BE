import asyncio
import json
from time import sleep

from asgiref.sync import sync_to_async
from channels.generic.websocket import (AsyncJsonWebsocketConsumer,
                                        JsonWebsocketConsumer, async_to_sync)

from core.utility import *
from room.models import Message, Room
from user.models import User


class GptResponseGenerator(AsyncJsonWebsocketConsumer):
    async def send_sentence(self, messages, sentence):
        messages = add_assistant_message_to_messages(
            messages, sentence)
        output_audio_url = get_audio_file_url_using_inference(sentence)
        await self.send_output_text(sentence)
        print_colored(f'SEND OUTPUT TEXT : {sentence}', "yellow")
        await self.send_audio_url(output_audio_url)
        print_colored(f"SEND AUDIO URL : {output_audio_url}", "yellow")
        await sync_to_async(Message.objects.create)(
            room=self.room, audio_url=output_audio_url, text=sentence, role='assistant')

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

        prompt = "Role: 당신은 ‘어린아이의 상상 속에 존재하는 친근한 친구’입니다.\
            Task: 당신은 어린아이의 사회성 발달을 위해 친근한 친구의 이미지로 즐겁게 대화를 나눠야 합니다. 어린아이가 이해하기 어려울만한 어려운 단어를 사용하지 마세요. 또, 존댓말을 사용하지 말고 친근한 어투로 말해주세요.\
            Note: 너무 많은 말을 하지 마세요. 답변의 길이는 최대 3문장으로 제한해주세요. 상대가 어린아이임을 고려하여 잘못된 인식을 심어줄 수 있는 주제는 다루지 마세요. 느낌표와 이모티콘 사용은 최대한 배제하도록 해주세요.\
            이제 어린아이와의 대화를 시작하겠습니다. 반갑게 인사하면서 간단한 질문을 던져주세요. 다음은 예시 답변입니다.\
            ```안녕. 반가워. 오늘 하루는 어땠어?```"
        await self.room.set_system(prompt)

        await self.accept()

        hello_sentence = f"안녕! 반가워!"
        messages = await self.room.get_messages()
        await self.send_sentence(messages, hello_sentence)

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

        messages = await self.room.get_messages()
        messages = add_user_message_to_messages(
            messages, text_gotten_by_input_data)
        sent_sentence = ""
        for sentence in get_sentences_by_chatgpt(messages):
            if sentence.strip() == "":
                continue
            sent_sentence += sentence
            if len(sent_sentence) <= 15:
                continue
            await self.send_sentence(messages, sent_sentence)
            sent_sentence = ""
        if sent_sentence != "":
            await self.send_sentence(messages, sent_sentence)
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
        messages = await self.room.get_messages()
        print_colored(messages, "red")
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
