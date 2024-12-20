from datetime import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from django.db import connection
#
# from Chat.models import ChatContent, ChatContentDetail, Chat
# import json
#
# from Common import jwt_auth
# from Common.PushManager import PushManager
# from Common.logger import app_log
# from Admin.models import AdminUser
# from User.models import Users, PushUserToken, PushNotifications
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     user = ''
#     chats = dict()
#
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['user_id']
#         self.admin_id = self.scope['url_route']['kwargs']['admin_id']
#         self.origin = self.scope['url_route']['kwargs']['origin']
#         app_log.info(f":admin:{self.admin_id}, user:{self.room_name},origin:{self.origin}")
#
#         if self.room_name and self.admin_id and self.origin:
#             app_log.info(f"open chat")
#             await self.channel_layer.group_add(
#                 self.room_name,
#                 self.channel_name
#             )
#
#             await self.channel_layer.group_add(
#                 self.admin_id,
#                 self.channel_name
#             )
#             try:
#                 ChatConsumer.chats[self.room_name].add(self)
#             except:
#                 ChatConsumer.chats[self.room_name] = set([self])
#
#             await self.accept()
#             message = self.read_history(self.room_name, self.admin_id, self.origin)
#             await self.send(text_data=json.dumps({
#                 'message': message
#             }))
#             await self.channel_layer.group_send(
#                 self.admin_id,
#                 {
#                     'type': 'push_message',
#                     'message': message
#                 }
#             )
#         else:
#             app_log.info(f"close chat")
#             await self.close()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name,
#             self.channel_name
#         )
#         ChatConsumer.chats[self.room_name].remove(self)
#         app_log.info(f"close chat")
#         await self.close()
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         app_log.info(f"Receive message from WebSocket data:{text_data_json}")
#         if self.origin == 'web':
#             text_data_json['origin'] = 1
#         else:
#             text_data_json['origin'] = 2
#         msg, chat, reply_content, msg1 = self.save_content(text_data_json)
#         if len(ChatConsumer.chats[self.room_name]) >= 2:
#             msg1.is_read = 1
#             msg1.save()
#         if reply_content:
#             reply = reply_content.chat_content.content_text
#         else:
#             reply = ''
#         if text_data_json['id']:
#             is_edit = 1
#         else:
#             is_edit = 0
#         text_data_json1 = {}
#         text_data_json1["chat_id"] = msg.id
#         text_data_json1["content"] = msg.chat_content.content_text
#         text_data_json1["reply"] = reply
#         text_data_json1["is_edit"] = is_edit
#         text_data_json1["to_id"] = text_data_json["to_id"]
#         text_data_json1["from_id"] = text_data_json["from_id"]
#         text_data_json1["created_at"] = msg.created_at.strftime("%Y-%m-%d %H:%M")
#         text_date_str = json.dumps(text_data_json1)
#         await self.channel_layer.group_send(
#             self.room_name,
#             {
#                 'type': 'chat_message',
#                 'message': text_date_str
#             }
#         )
#
#         await self.channel_layer.group_send(
#             self.admin_id,
#             {
#                 'type': 'push_message',
#                 'message': text_date_str
#             }
#         )
#
#     async def push_message(self, event):
#         message = ''
#         await self.send(message)
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         message_json = json.loads(message)
#         app_log.info(f"Receive message from room group data:{message_json}")
#         admin_id = int(self.admin_id)
#         user_id = int(self.room_name)
#         from_id = int(message_json['from_id'])
#         to_id = int(message_json['to_id'])
#         user = Users.objects.filter(id=user_id).first()
#         admin = AdminUser.objects.filter(id=admin_id).first()
#         if self.origin == 'web' and from_id == admin_id:
#             message_json['is_initiator'] = 1
#             message_json['full_name'] = admin.name
#             message_json['file_name'] = admin.file_name
#             self.push_chat_notification(user_id)
#         if self.origin == 'web' and to_id == admin_id:
#             message_json['is_initiator'] = 0
#             message_json['full_name'] = user.full_name
#             message_json['file_name'] = user.file_name
#         if self.origin == 'app' and to_id == user_id:
#             message_json['is_initiator'] = 0
#             message_json['full_name'] = admin.name
#             message_json['file_name'] = admin.file_name
#         if self.origin == 'app' and from_id == user_id:
#             message_json['is_initiator'] = 1
#             message_json['full_name'] = user.full_name
#             message_json['file_name'] = user.file_name
#         message = json.dumps(message_json)
#         # Send message to WebSocket。
#         app_log.info(f"Send message to WebSocket data:{message_json}")
#         await self.send(message)
#
#     def verify_token(self, user_id, admin_id, origin):
#         if origin == 'web':
#             admin_user = AdminUser.objects.filter(id=admin_id).first()
#             check_ret = jwt_auth.parse_payload(admin_user.access_token)
#             if check_ret.get("status"):
#                 result = 1
#             else:
#                 result = 0
#         else:
#             app_user = Users.objects.filter(id=user_id).first()
#             check_ret = jwt_auth.parse_payload(app_user.access_token)
#             if check_ret.get("status"):
#                 result = 1
#             else:
#                 result = 0
#         connection.close()
#         return result
#
#     def push_chat_notification(self, user_id):
#         app_log.info(f"chat push notification ")
#         push_notifications = PushUserToken.objects.filter(user_id=user_id).first()
#         u = Users.objects.get(id=user_id)
#         if push_notifications:
#             notify = PushNotifications(
#                 user=u,
#                 user_agent=push_notifications.user_agent,
#                 registration_token=push_notifications.token,
#                 message_data={"page": "Chat"},
#                 title="Chat",
#                 body="You have a new message from your care manager",
#                 section="Chat",  # "home", "update", "community" "journey", "education
#             )
#             notify.save()
#             try:
#                 PushManager.push_message_with_push_notification(notify, badge=1)
#             except Exception as e:
#                 app_log.exception(e)
#         else:
#             app_log.info("user token is null:{}".format(u.id))
#
#     def save_content(self, text_data_json):
#         to_id = text_data_json['to_id']
#         from_id = text_data_json['from_id']
#         content = text_data_json['content']
#         reply_id = text_data_json['reply_id'] if text_data_json['reply_id'] else 0
#         edit_id = text_data_json['id']
#         origin = text_data_json['origin']
#         if origin == 1:
#             chat = Chat.objects.filter(user_id=to_id, admin_user_id=from_id).first()
#         else:
#             chat = Chat.objects.filter(user_id=from_id, admin_user_id=to_id).first()
#         reply_content = ChatContent.objects.filter(id=reply_id).first()
#         if not chat:
#             if origin == 1:
#                 chat = Chat.objects.create(user_id=to_id, admin_user_id=from_id)
#             else:
#                 chat = Chat.objects.create(user_id=from_id, admin_user_id=to_id)
#         if edit_id:
#             msg = ChatContent.objects.filter(id=edit_id).first()
#             ChatContentDetail.objects.filter(id=msg.chat_content_id).update(content_text=content)
#             ChatContent.objects.filter(chat_content_id=msg.chat_content_id).update(is_edit=1)
#             msg1 = ChatContent.objects.filter(chat_content_id=msg.chat_content_id, is_initiator=1).first()
#         else:
#             detail = ChatContentDetail.objects.create(content_text=content)
#             if origin == 1:
#                 msg = ChatContent.objects.create(admin_user_id=from_id, user_id=to_id,
#                                                  chat_content_id=detail.id, chat_id=chat.id, is_initiator=1,
#                                                  reply_id=reply_id, origin=1)
#                 msg1 = ChatContent.objects.create(admin_user_id=from_id, user_id=to_id,
#                                                   chat_content_id=detail.id, chat_id=chat.id, is_initiator=0,
#                                                   reply_id=reply_id, origin=1)
#             else:
#                 msg = ChatContent.objects.create(admin_user_id=to_id, user_id=from_id,
#                                                  chat_content_id=detail.id, chat_id=chat.id, is_initiator=1,
#                                                  reply_id=reply_id, origin=2)
#                 msg1 = ChatContent.objects.create(admin_user_id=to_id, user_id=from_id,
#                                                   chat_content_id=detail.id, chat_id=chat.id, is_initiator=0,
#                                                   reply_id=reply_id, origin=2)
#         Chat.objects.filter(id=chat.id).update(updated_at=datetime.utcnow())
#         if msg.reply_id:
#             reply_content = ChatContent.objects.filter(id=msg.reply_id).first()
#         return msg, chat, reply_content, msg1
#
#     def read_history(self, user_id, admin_id, origin):
#         message = []
#         if origin == 'web':
#             chat_records = ChatContent.objects.filter(
#                 Q(admin_user_id=admin_id, user_id=user_id, origin=1, is_initiator=1) | Q(admin_user_id=admin_id,
#                                                                                          user_id=user_id, origin=2,
#                                                                                          is_initiator=0)
#             ).all().order_by('id')
#         else:
#             chat_records = ChatContent.objects.filter(
#                 Q(admin_user_id=admin_id, user_id=user_id, origin=2, is_initiator=1) | Q(admin_user_id=admin_id,
#                                                                                          user_id=user_id, origin=1,
#                                                                                          is_initiator=0)
#             ).all().order_by('id')
#         connection.close()
#         for chat_ in chat_records:
#             if chat_.is_initiator == 0 and chat_.is_read == 0:
#                 ChatContent.objects.filter(id=chat_.id).update(is_read=1)
#             if chat_.origin == 1:
#                 full_name = chat_.admin_user.name
#             else:
#                 full_name = chat_.user.full_name
#             if chat_.reply_id:
#                 chat_content = ChatContent.objects.filter(id=chat_.reply_id).first()
#                 chat_detail = ChatContentDetail.objects.filter(id=chat_content.chat_content_id).first()
#                 reply = chat_detail.content_text
#             else:
#                 reply = ''
#             ret = {
#                 "chat_id": chat_.id,
#                 "is_initiator": chat_.is_initiator,
#                 "full_name": full_name,
#                 "file_name": chat_.user.file_name,
#                 "content": chat_.chat_content.content_text,
#                 "reply": reply,
#                 "is_edit": chat_.is_edit,
#                 "created_at": chat_.chat_content.created_at.strftime("%Y-%m-%d %H:%M"),
#             }
#             message.append(ret)
#         app_log.info(f"chat history data:{message}")
#         return message
#
#
# class ChatUnread(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         self.admin = self.scope['url_route']['kwargs']['admin']
#         if self.admin:
#             await self.channel_layer.group_add(
#                 self.admin,
#                 self.channel_name
#             )
#             await self.accept()
#             ret = self.get_unread_count(self.admin)
#             message = ret
#             await self.send(text_data=json.dumps({
#                 'message': message
#             }))
#         else:
#             await self.close()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.admin,
#             self.channel_name
#         )
#         await self.close()
#
#     async def push_message(self, event):
#         ret = self.get_unread_count(self.admin)
#         await self.send(text_data=json.dumps({
#             'message': ret
#         }))
#
#     def get_unread(self, admin):
#         ret = []
#         user_ids = []
#         chat_contents = ChatContent.objects.filter(admin_user_id=admin, is_read=0, is_initiator=0, origin=2).all()
#         connection.close()
#         for user_ in chat_contents:
#             if user_.user.id not in user_ids:
#                 user_ids.append(user_.user.id)
#                 unread = ChatContent.objects.filter(admin_user_id=admin,
#                                                     is_initiator=0, is_read=0, user_id=user_.user.id,
#                                                     origin=2).all().count()
#                 res = {
#                     "id": user_.id,
#                     "user_id": user_.user.id,
#                     "full_name": user_.user.full_name,
#                     "file_name": user_.user.file_name,
#                     "starred": user_.chat.starred,
#                     "unread": unread,
#                     "latest_at": user_.updated_at.strftime("%Y-%m-%d"),
#                 }
#                 ret.append(res)
#         return ret
#
#     def get_unread_count(self, admin):
#         ret = {}
#         chat_contents = ChatContent.objects.filter(admin_user_id=admin, is_read=0, is_initiator=0,
#                                                    origin=2).all()
#         app_log.info(f'\n\nChatUnread: get_unread_count: {chat_contents.count()}, admin: {self.admin}\n\n')
#         ret['count'] = chat_contents.count()
#         connection.close()
#         return ret
#
#     def get_starred_users(self, admin):
#         ret = []
#         chat_users = Chat.objects.filter(admin_user_id=admin, starred=1).all().order_by('-updated_at')
#         connection.close()
#         for user_ in chat_users:
#             unread = ChatContent.objects.filter(admin_user_id=admin,
#                                                 is_initiator=0, is_read=0, user_id=user_.user.id,
#                                                 origin=2).all().count()
#             res = {
#                 "user_id": user_.user.id,
#                 "full_name": user_.user.full_name,
#                 "file_name": user_.user.file_name,
#                 "starred": user_.starred,
#                 "unread": unread,
#                 "latest_at": user_.updated_at.strftime("%Y-%m-%d"),
#             }
#             ret.append(res)
#         return ret
#
#     def get_all_users(self, admin):
#         ret = []
#         chat_user_ids = []
#         chat_users = Chat.objects.filter(admin_user_id=admin).all().order_by('-updated_at')
#         connection.close()
#         for user_ in chat_users:
#             unread = ChatContent.objects.filter(admin_user_id=admin,
#                                                 is_initiator=0, is_read=0, user_id=user_.user.id,
#                                                 origin=2).all().count()
#             res = {
#                 "user_id": user_.user.id,
#                 "full_name": user_.user.full_name,
#                 "file_name": user_.user.file_name,
#                 "starred": user_.starred,
#                 "unread": unread,
#                 "latest_at": user_.updated_at.strftime("%Y-%m-%d"),
#             }
#             ret.append(res)
#             chat_user_ids.append(user_.user_id)
#         other_users = Users.objects.filter(care_manager_id=admin).all().exclude(id__in=chat_user_ids)
#         connection.close()
#         for u in other_users:
#             res = {
#                 "user_id": u.id,
#                 "full_name": u.full_name,
#                 "file_name": u.file_name,
#                 "unread": 0,
#                 "latest_at": u.updated_at.strftime("%Y-%m-%d"),
#             }
#             ret.append(res)
#         return ret


from asgiref.sync import sync_to_async
from .models import ChatConnection, Messages
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group (channel layer)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.accept()

        # Fetch and send chat history
        chat_history = await self.fetch_chat_history(self.room_name)
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'messages': chat_history
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        user_id = text_data_json.get('userId')
        sender_name = text_data_json.get('senderName')

        # Store the message in the database using sync_to_async
        await self.save_message_to_db(message, self.room_name, text_data_json.get('link'), text_data_json.get('link_type'), user_id)

        # Send the message to the room group (channel layer)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'userId': user_id,
                'senderName': sender_name
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def fetch_chat_history(self, room_name):
        """Fetches the chat history for a given room."""
        try:
            chat_connection = ChatConnection.objects.get(chat_room=room_name)
            messages = Messages.objects.filter(chat_room_connection=chat_connection).order_by('created_at')
            return [
                {
                    'message': message.messages,
                    'senderName': message.send_by.name,  # adjust as needed
                    'timestamp': message.created_at.isoformat(),
                    'link': message.link,
                    'link_type': message.link_type,
                    'userId': message.send_by.id
                }
                for message in messages
            ]
        except ChatConnection.DoesNotExist:
            return []

    @sync_to_async
    def save_message_to_db(self, message, room_name, link, link_type, userId):
        """Save a message to the database."""
        chat_connection, _ = ChatConnection.objects.get_or_create(chat_room=room_name)
        Messages.objects.create(
            messages=message,
            chat_room_connection=chat_connection,
            link=link,
            link_type=link_type,
            send_by_id=userId
        )
