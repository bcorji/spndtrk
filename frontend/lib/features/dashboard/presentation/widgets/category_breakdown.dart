import 'package:flutter/material.dart';
import 'package:intl/intl.dart';


class CategoryBreakdown extends StatelessWidget {
  final List<dynamic> categories;
  final String currency;

  const CategoryBreakdown({
    super.key,
    required this.categories,
    required this.currency,
  });

  String formatMoney(dynamic value) {
    final amount = double.parse(value.toString());

    return NumberFormat.currency(
      name: currency,
      decimalDigits: 2,
    ).format(amount);
  }

  @override
  Widget build(BuildContext context) {
    if (categories.isEmpty) {
      return const Text(
        'No expense data available for this period.',
      );
    }

    return Column(
      children: categories.map((item) {
        final category = item as Map<String, dynamic>;

        final percentage = (
          category['percentage'] as num
        ).toDouble();

        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(category['category'].toString()),
                  ),
                  Text(formatMoney(category['total'])),
                ],
              ),

              const SizedBox(height: 8),

              LinearProgressIndicator(
                value: (percentage / 100).clamp(0.0, 1.0),
                minHeight: 8,
                borderRadius: BorderRadius.circular(8),
              ),

              const SizedBox(height: 4),

              Text(
                '${percentage.toStringAsFixed(1)}%',
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}