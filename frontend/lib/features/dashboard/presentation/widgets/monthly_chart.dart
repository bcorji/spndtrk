import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';


class MonthlyChart extends StatelessWidget {
  final List<dynamic> data;

  const MonthlyChart({
    super.key,
    required this.data,
  });

  @override
  Widget build(BuildContext context) {
    final groups = data.asMap().entries.map((entry) {
      final index = entry.key;
      final item = entry.value as Map<String, dynamic>;

      final income = double.parse(
        item['income'].toString(),
      );

      final expenses = double.parse(
        item['expenses'].toString(),
      );

      return BarChartGroupData(
        x: index,
        barsSpace: 4,
        barRods: [
          BarChartRodData(
            toY: income,
            width: 8,
            borderRadius: BorderRadius.circular(4),
          ),
          BarChartRodData(
            toY: expenses,
            width: 8,
            borderRadius: BorderRadius.circular(4),
          ),
        ],
      );
    }).toList();

    return SizedBox(
      height: 250,
      child: BarChart(
        BarChartData(
          barGroups: groups,
          alignment: BarChartAlignment.spaceAround,
          gridData: const FlGridData(
            show: true,
          ),
          borderData: FlBorderData(
            show: false,
          ),
          titlesData: FlTitlesData(
            topTitles: const AxisTitles(
              sideTitles: SideTitles(
                showTitles: false,
              ),
            ),
            rightTitles: const AxisTitles(
              sideTitles: SideTitles(
                showTitles: false,
              ),
            ),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                getTitlesWidget: (value, meta) {
                  final index = value.toInt();

                  if (index < 0 || index >= data.length) {
                    return const SizedBox.shrink();
                  }

                  final month = data[index]['month'].toString();

                  return Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Text(
                      month.substring(5),
                      style: const TextStyle(fontSize: 11),
                    ),
                  );
                },
              ),
            ),
          ),
        ),
      ),
    );
  }
}