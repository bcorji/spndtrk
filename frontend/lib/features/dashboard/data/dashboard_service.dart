import 'package:dio/dio.dart';


class DashboardService {
  final Dio dio;

  DashboardService(this.dio);

  Future<Map<String, dynamic>> getSummary({
    required String currency,
  }) async {
    final response = await dio.get(
      '/analytics/summary',
      queryParameters: {
        'currency': currency,
      },
    );

    return Map<String, dynamic>.from(response.data);
  }

  Future<Map<String, dynamic>> getTrends({
    required String currency,
    int months = 6,
  }) async {
    final response = await dio.get(
      '/analytics/trends',
      queryParameters: {
        'currency': currency,
        'months': months,
      },
    );

    return Map<String, dynamic>.from(response.data);
  }

  Future<Map<String, dynamic>> getCategories({
    required String currency,
  }) async {
    final response = await dio.get(
      '/analytics/categories',
      queryParameters: {
        'currency': currency,
      },
    );

    return Map<String, dynamic>.from(response.data);
  }

  Future<List<dynamic>> getRecentTransactions() async {
    final response = await dio.get(
      '/transactions/',
      queryParameters: {
        'skip': 0,
        'limit': 5,
      },
    );

    return List<dynamic>.from(response.data);
  }
}