# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/chat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11protos/chat.proto\x12\x04grpc\"@\n\x08\x42\x36\x34Image\x12\x10\n\x08\x62\x36\x34image\x18\x01 \x01(\t\x12\x15\n\x08mimeType\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_mimeType\"H\n\x08Greeting\x12\x0c\n\x04nick\x18\x01 \x01(\t\x12\x12\n\x05group\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x08last_ack\x18\x03 \x01(\x05\x42\x08\n\x06_group\"\xc9\x01\n\x03Msg\x12\x12\n\x05msgID\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x0c\n\x04nick\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\"\n\x05image\x18\x05 \x01(\x0b\x32\x0e.grpc.B64ImageH\x01\x88\x01\x01\x12\x15\n\x08priority\x18\x06 \x01(\tH\x02\x88\x01\x01\x12\x14\n\x07replyID\x18\x07 \x01(\tH\x03\x88\x01\x01\x42\x08\n\x06_msgIDB\x08\n\x06_imageB\x0b\n\t_priorityB\n\n\x08_replyID\"\x07\n\x05\x45mpty2\x8a\x01\n\x04\x43hat\x12$\n\x08send_msg\x12\t.grpc.Msg\x1a\x0b.grpc.Empty\"\x00\x12,\n\x0breceive_msg\x12\x0e.grpc.Greeting\x1a\t.grpc.Msg\"\x00\x30\x01\x12.\n\rclient_update\x12\x0e.grpc.Greeting\x1a\x0b.grpc.Empty\"\x00\x62\x06proto3')



_B64IMAGE = DESCRIPTOR.message_types_by_name['B64Image']
_GREETING = DESCRIPTOR.message_types_by_name['Greeting']
_MSG = DESCRIPTOR.message_types_by_name['Msg']
_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
B64Image = _reflection.GeneratedProtocolMessageType('B64Image', (_message.Message,), {
  'DESCRIPTOR' : _B64IMAGE,
  '__module__' : 'protos.chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.B64Image)
  })
_sym_db.RegisterMessage(B64Image)

Greeting = _reflection.GeneratedProtocolMessageType('Greeting', (_message.Message,), {
  'DESCRIPTOR' : _GREETING,
  '__module__' : 'protos.chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Greeting)
  })
_sym_db.RegisterMessage(Greeting)

Msg = _reflection.GeneratedProtocolMessageType('Msg', (_message.Message,), {
  'DESCRIPTOR' : _MSG,
  '__module__' : 'protos.chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Msg)
  })
_sym_db.RegisterMessage(Msg)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'protos.chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Empty)
  })
_sym_db.RegisterMessage(Empty)

_CHAT = DESCRIPTOR.services_by_name['Chat']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _B64IMAGE._serialized_start=27
  _B64IMAGE._serialized_end=91
  _GREETING._serialized_start=93
  _GREETING._serialized_end=165
  _MSG._serialized_start=168
  _MSG._serialized_end=369
  _EMPTY._serialized_start=371
  _EMPTY._serialized_end=378
  _CHAT._serialized_start=381
  _CHAT._serialized_end=519
# @@protoc_insertion_point(module_scope)