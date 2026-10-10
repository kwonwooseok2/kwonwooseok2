import 'package:flutter/material.dart';
import 'package:peachtalk/core/router/app_router.dart';
import 'package:peachtalk/core/theme/peach_theme.dart';

class PeachTalkApp extends StatelessWidget {
  const PeachTalkApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: '피치톡',
      debugShowCheckedModeBanner: false,
      theme: PeachTheme.light,
      darkTheme: PeachTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: appRouter,
    );
  }
}
