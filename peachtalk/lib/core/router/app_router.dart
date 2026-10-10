import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:peachtalk/features/auth/login_page.dart';
import 'package:peachtalk/features/chat/chat_room_page.dart';
import 'package:peachtalk/features/home/home_shell.dart';

final appRouter = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: '/home',
      builder: (context, state) => const HomeShell(),
    ),
    GoRoute(
      path: '/chat/:roomId',
      builder: (context, state) {
        final id = state.pathParameters['roomId']!;
        final title = state.uri.queryParameters['title'] ?? '채팅';
        return ChatRoomPage(roomId: id, title: title);
      },
    ),
  ],
  errorBuilder: (context, state) => Scaffold(
    body: Center(child: Text('페이지 없음: ${state.error}')),
  ),
);
