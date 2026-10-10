import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// 피치톡 브랜드 — 복숭아 살구톤. 보라/크림 AI 기본룩 회피.
class PeachTheme {
  static const peach = Color(0xFFFF8A65);
  static const peachDeep = Color(0xFFE85D3B);
  static const cream = Color(0xFFFFF4EE);
  static const ink = Color(0xFF1F1410);
  static const mist = Color(0xFFFFE0D4);

  static ThemeData get light {
    final base = ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: peach,
        primary: peachDeep,
        secondary: peach,
        surface: cream,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: cream,
    );
    return base.copyWith(
      textTheme: GoogleFonts.notoSansKrTextTheme(base.textTheme).apply(
        bodyColor: ink,
        displayColor: ink,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: cream,
        foregroundColor: ink,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.notoSansKr(
          fontWeight: FontWeight.w800,
          fontSize: 22,
          color: ink,
        ),
      ),
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: peachDeep,
        foregroundColor: Colors.white,
      ),
    );
  }

  static ThemeData get dark {
    final base = ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: ColorScheme.fromSeed(
        seedColor: peach,
        primary: peach,
        secondary: mist,
        surface: const Color(0xFF1A1210),
        brightness: Brightness.dark,
      ),
    );
    return base.copyWith(
      textTheme: GoogleFonts.notoSansKrTextTheme(base.textTheme),
    );
  }
}
