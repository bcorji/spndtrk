import 'package:dio/dio.dart';

import '../../../core/network/token_storage.dart';


class AuthService {
  final Dio dio;

  AuthService(this.dio);

  Future<Map<String, dynamic>> register({
    required String email,
    required String fullName,
    required String password,
  }) async {
    final response = await dio.post(
      '/auth/register',
      data: {
        'email': email,
        'full_name': fullName,
        'password': password,
      },
    );

    return Map<String, dynamic>.from(response.data);
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await dio.post(
      '/auth/login',
      data: {
        'email': email,
        'password': password,
      },
    );

    final data = Map<String, dynamic>.from(response.data);

    await TokenStorage().saveToken(
      data['access_token'] as String,
    );

    return data;
  }

  Future<Map<String, dynamic>> getCurrentUser() async {
    final response = await dio.get('/users/me');

    return Map<String, dynamic>.from(response.data);
  }

  Future<void> logout() async {
    await TokenStorage().deleteToken();
  }
}