import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../providers/dashboard_provider.dart';

import 'widgets/summary_card.dart';
import 'widgets/monthly_chart.dart';
import 'widgets/category_breakdown.dart';
import 'widgets/recent_transactions.dart';


class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() =>
      _DashboardScreenState();
}


class _DashboardScreenState extends ConsumerState<DashboardScreen> {

  String currency = 'NGN';

  String formatMoney(dynamic value) {
    final amount = double.parse(value.toString());

    return NumberFormat.currency(
      name: currency,
      decimalDigits: 2,
    ).format(amount);
  }

  Future<void> refreshDashboard() async {
    ref.invalidate(summaryProvider(currency));
    ref.invalidate(trendsProvider(currency));
    ref.invalidate(categoriesProvider(currency));
    ref.invalidate(recentTransactionsProvider);

    await Future.wait([
      ref.read(summaryProvider(currency).future),
      ref.read(trendsProvider(currency).future),
      ref.read(categoriesProvider(currency).future),
      ref.read(recentTransactionsProvider.future),
    ]);
  }

  @override
  Widget build(BuildContext context) {

    final summary = ref.watch(summaryProvider(currency));
    final trends = ref.watch(trendsProvider(currency));
    final categories = ref.watch(categoriesProvider(currency));
    final transactions = ref.watch(recentTransactionsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Expense Tracker'),
        actions: [
          DropdownButton<String>(
            value: currency,
            underline: const SizedBox.shrink(),
            items: const [
              DropdownMenuItem(
                value: 'NGN',
                child: Text('NGN'),
              ),
              DropdownMenuItem(
                value: 'USD',
                child: Text('USD'),
              ),
              DropdownMenuItem(
                value: 'GBP',
                child: Text('GBP'),
              ),
            ],
            onChanged: (value) {
              if (value != null) {
                setState(() {
                  currency = value;
                });
              }
            },
          ),

          const SizedBox(width: 12),
        ],
      ),

      body: RefreshIndicator(
        onRefresh: refreshDashboard,

        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),

          padding: const EdgeInsets.all(16),

          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,

            children: [

              Text(
                'Financial Overview',
                style: Theme.of(context).textTheme.headlineSmall,
              ),

              const SizedBox(height: 8),

              Text(
                'Here is your financial summary.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),

              const SizedBox(height: 20),

              summary.when(
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),

                error: (error, stack) => Text(
                  'Unable to load summary: $error',
                ),

                data: (data) {

                  final income = data['total_income'];
                  final expenses = data['total_expenses'];
                  final balance = data['net_balance'];
                  final count = data['transaction_count'];

                  return Column(
                    children: [

                      GridView.count(
                        crossAxisCount: 2,
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        childAspectRatio: 1.25,

                        children: [

                          SummaryCard(
                            title: 'Total Income',
                            amount: formatMoney(income),
                            icon: Icons.trending_up,
                            color: Colors.green,
                          ),

                          SummaryCard(
                            title: 'Total Expenses',
                            amount: formatMoney(expenses),
                            icon: Icons.trending_down,
                            color: Colors.red,
                          ),

                          SummaryCard(
                            title: 'Net Balance',
                            amount: formatMoney(balance),
                            icon: Icons.account_balance_wallet,
                            color: Colors.blue,
                          ),

                          SummaryCard(
                            title: 'Transactions',
                            amount: count.toString(),
                            icon: Icons.receipt_long,
                            color: Colors.orange,
                          ),
                        ],
                      ),
                    ],
                  );
                },
              ),

              const SizedBox(height: 28),

              Text(
                'Income vs Expenses',
                style: Theme.of(context).textTheme.titleLarge,
              ),

              const SizedBox(height: 16),

              trends.when(
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),

                error: (error, stack) => Text(
                  'Unable to load trends: $error',
                ),

                data: (data) => MonthlyChart(
                  data: data['data'] as List<dynamic>,
                ),
              ),

              const SizedBox(height: 28),

              Text(
                'Spending by Category',
                style: Theme.of(context).textTheme.titleLarge,
              ),

              const SizedBox(height: 16),

              categories.when(
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),

                error: (error, stack) => Text(
                  'Unable to load categories: $error',
                ),

                data: (data) => CategoryBreakdown(
                  categories: data['data'] as List<dynamic>,
                  currency: currency,
                ),
              ),

              const SizedBox(height: 28),

              Text(
                'Recent Transactions',
                style: Theme.of(context).textTheme.titleLarge,
              ),

              const SizedBox(height: 12),

              transactions.when(
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),

                error: (error, stack) => Text(
                  'Unable to load transactions: $error',
                ),

                data: (data) => RecentTransactions(
                  transactions: data,
                ),
              ),

              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    );
  }
}