import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'features/auth/presentation/login_screen.dart';


void main() {
  runApp(
    const ProviderScope(
      child: ExpenseTrackerApp(),
    ),
  );
}


class ExpenseTrackerApp extends StatelessWidget {
  const ExpenseTrackerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SpndTrk',

      debugShowCheckedModeBanner: false,

      theme: ThemeData(
        useMaterial3: true,

        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
        ),

        scaffoldBackgroundColor: Colors.white,
      ),

      home: const LoginScreen(),
    );
  }
}