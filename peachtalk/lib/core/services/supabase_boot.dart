import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseBoot {
  static bool ready = false;

  /// `.env` 또는 `--dart-define` 로 주입. 없으면 로컬 목업 모드.
  static Future<void> init() async {
    const url = String.fromEnvironment('SUPABASE_URL');
    const anon = String.fromEnvironment('SUPABASE_ANON_KEY');
    if (url.isEmpty || anon.isEmpty) {
      debugPrint('[피치톡] Supabase 키 없음 → 오프라인 목업 모드');
      ready = false;
      return;
    }
    await Supabase.initialize(url: url, anonKey: anon);
    ready = true;
  }

  static SupabaseClient? get client =>
      ready ? Supabase.instance.client : null;
}
