import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:peachtalk/core/models/chat_models.dart';
import 'package:peachtalk/core/theme/peach_theme.dart';

class ChatListPage extends StatelessWidget {
  const ChatListPage({super.key});

  static final _mock = [
    ChatRoomPreview(
      id: 'r1',
      title: '민지',
      lastMessage: '오늘 저녁 가능해요?',
      updatedAt: DateTime.now().subtract(const Duration(minutes: 4)),
      unread: 2,
    ),
    ChatRoomPreview(
      id: 'r2',
      title: '피치 모임',
      lastMessage: '사진 올렸어요 🍑',
      updatedAt: DateTime.now().subtract(const Duration(hours: 1)),
    ),
    ChatRoomPreview(
      id: 'r3',
      title: '준호',
      lastMessage: '네 확인했어요',
      updatedAt: DateTime.now().subtract(const Duration(days: 1)),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('피치톡'),
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.search_rounded),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.edit_rounded),
      ),
      body: ListView.separated(
        itemCount: _mock.length,
        separatorBuilder: (_, __) => const Divider(height: 1, indent: 76),
        itemBuilder: (context, i) {
          final room = _mock[i];
          return ListTile(
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            leading: CircleAvatar(
              radius: 26,
              backgroundColor: PeachTheme.mist,
              child: Text(
                room.title.characters.first,
                style: const TextStyle(
                  color: PeachTheme.peachDeep,
                  fontWeight: FontWeight.w800,
                  fontSize: 18,
                ),
              ),
            ),
            title: Text(
              room.title,
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            subtitle: Text(
              room.lastMessage,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  _timeLabel(room.updatedAt),
                  style: TextStyle(
                    fontSize: 12,
                    color: PeachTheme.ink.withValues(alpha: 0.45),
                  ),
                ),
                if (room.unread > 0) ...[
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: PeachTheme.peachDeep,
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      '${room.unread}',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 11,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ],
              ],
            ),
            onTap: () => context.push(
              '/chat/${room.id}?title=${Uri.encodeComponent(room.title)}',
            ),
          );
        },
      ),
    );
  }

  String _timeLabel(DateTime t) {
    final d = DateTime.now().difference(t);
    if (d.inMinutes < 60) return '${d.inMinutes}분';
    if (d.inHours < 24) return '${d.inHours}시간';
    return '${d.inDays}일';
  }
}
