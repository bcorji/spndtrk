import 'package:dio/dio.dart';

class TransactionService {
  final Dio dio;

  TransactionService(this.dio);

  Future<List<dynamic>> getTransactions(
    String accessToken,
  ) async {
    final response = await dio.get(
      '/transactions/',
      options: Options(
        headers: {
          'Authorization': 'Bearer $accessToken',
        },
      ),
    );

    return response.data as List<dynamic>;
  }

  Future<Map<String, dynamic>> createTransaction({
    required String accessToken,
    required String amount,
    required String currency,
    required String type,
    required String description,
    required String transactionDate,
  }) async {
    final response = await dio.post(
      '/transactions/',
      data: {
        'amount': amount,
        'currency': currency,
        'type': type,
        'description': description,
        'category_id': null,
        'transaction_date': transactionDate,
      },
      options: Options(
        headers: {
          'Authorization': 'Bearer $accessToken',
        },
      ),
    );

    return Map<String, dynamic>.from(response.data);
  }
}