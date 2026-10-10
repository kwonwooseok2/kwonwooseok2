class ChatRoomPreview {
  const ChatRoomPreview({
    required this.id,
    required this.title,
    required this.lastMessage,
    required this.updatedAt,
    this.unread = 0,
  });

  final String id;
  final String title;
  final String lastMessage;
  final DateTime updatedAt;
  final int unread;
}

class ChatMessage {
  const ChatMessage({
    required this.id,
    required this.roomId,
    required this.senderId,
    required this.body,
    required this.createdAt,
    this.isMine = false,
  });

  final String id;
  final String roomId;
  final String senderId;
  final String body;
  final DateTime createdAt;
  final bool isMine;
}
