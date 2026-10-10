import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:peachtalk/app/app.dart';
import 'package:peachtalk/core/services/supabase_boot.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SupabaseBoot.init();
  runApp(const ProviderScope(child: PeachTalkApp()));
}
