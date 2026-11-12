import 'package:dio/dio.dart';

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

    return Map<String, dynamic>.from(response.data);
  }

  Future<Map<String, dynamic>> getCurrentUser(
    String accessToken,
  ) async {
    final response = await dio.get(
      '/users/me',
      options: Options(
        headers: {
          'Authorization': 'Bearer $accessToken',
        },
      ),
    );

    return Map<String, dynamic>.from(response.data);
  }
}