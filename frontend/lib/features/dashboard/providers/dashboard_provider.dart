import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/api_client.dart';
import '../data/dashboard_service.dart';


final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});


final dashboardServiceProvider = Provider<DashboardService>((ref) {
  final client = ref.watch(apiClientProvider);

  return DashboardService(client.dio);
});


final summaryProvider = FutureProvider.family<
    Map<String, dynamic>,
    String>((ref, currency) async {

  final service = ref.watch(dashboardServiceProvider);

  return service.getSummary(
    currency: currency,
  );
});


final trendsProvider = FutureProvider.family<
    Map<String, dynamic>,
    String>((ref, currency) async {

  final service = ref.watch(dashboardServiceProvider);

  return service.getTrends(
    currency: currency,
    months: 6,
  );
});


final categoriesProvider = FutureProvider.family<
    Map<String, dynamic>,
    String>((ref, currency) async {

  final service = ref.watch(dashboardServiceProvider);

  return service.getCategories(
    currency: currency,
  );
});


final recentTransactionsProvider = FutureProvider<
    List<dynamic>>((ref) async {

  final service = ref.watch(dashboardServiceProvider);

  return service.getRecentTransactions();
});