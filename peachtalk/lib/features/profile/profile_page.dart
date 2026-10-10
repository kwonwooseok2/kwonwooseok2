import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:peachtalk/core/theme/peach_theme.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('나')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const SizedBox(height: 8),
          Center(
            child: CircleAvatar(
              radius: 44,
              backgroundColor: PeachTheme.mist,
              child: Text(
                '나',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: PeachTheme.peachDeep,
                      fontWeight: FontWeight.w900,
                    ),
              ),
            ),
          ),
          const SizedBox(height: 14),
          Center(
            child: Text(
              '피치유저',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w800,
                  ),
            ),
          ),
          const SizedBox(height: 4),
          Center(
            child: Text(
              '@peach',
              style: TextStyle(color: PeachTheme.ink.withValues(alpha: 0.5)),
            ),
          ),
          const SizedBox(height: 28),
          Card(
            color: Colors.white,
            elevation: 0,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: BorderSide(color: PeachTheme.mist),
            ),
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.edit_outlined),
                  title: const Text('프로필 수정'),
                  onTap: () {},
                ),
                const Divider(height: 1),
                ListTile(
                  leading: const Icon(Icons.logout_rounded),
                  title: const Text('로그아웃'),
                  onTap: () => context.go('/login'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
