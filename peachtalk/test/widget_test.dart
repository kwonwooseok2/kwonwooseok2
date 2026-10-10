import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:peachtalk/app/app.dart';

void main() {
  testWidgets('피치톡 로그인 화면이 뜬다', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: PeachTalkApp()));
    expect(find.text('피치톡'), findsOneWidget);
    expect(find.text('시작하기'), findsOneWidget);
  });
}
