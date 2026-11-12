import 'package:flutter/material.dart';
import 'package:intl/intl.dart';


class RecentTransactions extends StatelessWidget {
  final List<dynamic> transactions;

  const RecentTransactions({
    super.key,
    required this.transactions,
  });

  @override
  Widget build(BuildContext context) {
    if (transactions.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(16),
        child: Text('No transactions recorded yet.'),
      );
    }

    return Column(
      children: transactions.map((item) {
        final transaction = item as Map<String, dynamic>;

        final isIncome = transaction['type'] == 'income';

        final amount = double.parse(
          transaction['amount'].toString(),
        );

        final date = DateTime.parse(
          transaction['transaction_date'].toString(),
        ).toLocal();

        final currency = transaction['currency'].toString();

        final formattedAmount = NumberFormat.currency(
          name: currency,
          decimalDigits: 2,
        ).format(amount);

        return ListTile(
          leading: CircleAvatar(
            child: Icon(
              isIncome ? Icons.arrow_downward : Icons.arrow_upward,
            ),
          ),

          title: Text(
            transaction['description']?.toString() ??
                'Untitled transaction',
          ),

          subtitle: Text(
            DateFormat('dd MMM yyyy').format(date),
          ),

          trailing: Text(
            '${isIncome ? '+' : '-'}$formattedAmount',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: isIncome ? Colors.green : null,
            ),
          ),
        );
      }).toList(),
    );
  }
}