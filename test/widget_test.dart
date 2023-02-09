// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:fl_chart/fl_chart.dart';

import 'package:starview/main.dart';

List<ScatterSpot>? plottedData(var data, var data2) {
  if (data?.x.length > 5) {
    List<ScatterSpot> m = List.generate(
        data?.x.length,
        (index) => ScatterSpot(
            data?.x.values.toList()[index], data?.y.values.toList()[index],
            color: Color.fromARGB(255, 255, 255, 255),
            radius: (4.5 - data?.mag.values.toList()[index]).toDouble()));
    // m.add(ScatterSpot(-0.7, 1, show: false));
    // m.add(ScatterSpot(0.7, -1, show: false));
    var planetsCol = {
      'mercury': Color.fromARGB(255, 219, 206, 202),
      'venus': Color.fromARGB(255, 165, 124, 27),
      'mars': Color.fromARGB(255, 69, 24, 4),
      'jupiter': Color.fromARGB(255, 188, 175, 178),
      'saturn': Color.fromRGBO(234, 214, 184, 1),
      'uranus': Color.fromARGB(255, 209, 231, 231),
      'neptune': Color.fromARGB(255, 75, 112, 221),
      'moon': Color.fromARGB(255, 254, 252, 215)
    };
    var planetsSize = {
      'mercury': 10,
      'venus': 13,
      'mars': 13,
      'jupiter': 20,
      'saturn': 18,
      'uranus': 15,
      'neptune': 15,
      'moon': 23
    };
    List<ScatterSpot> p = List.generate(
        data2?.x.length,
        (index) => ScatterSpot(
            data2?.x.values.toList()[index], data2?.y.values.toList()[index],
            color: planetsCol[data2?.name.values.toList()[index].toLowerCase()],
            radius: planetsSize[data2.name.values.toList()[index].toLowerCase()]
                ?.toDouble(),
            show: true));
    List<dynamic> a1 = data?.name.values.toList();
    List<dynamic> a2 = data2?.name.values.toList();
    // labels = a1 + a2;
    // labels.add('Unknown');
    List<ScatterSpot> combined = m + p;
    return combined;
  } else {
    return null;
  }
}

void main() {
  void testValidResponse() async {
    final url = Uri.parse('http://10.0.2.2:5000/stars?normal=1:1:1');
    final response = await http.get(url).timeout(Duration(milliseconds: 30));
    expect(response.statusCode, 200);
  }

  void testErrorResponse() async {
    final url = Uri.parse('http://10.0.2.2:5000/stars?normal=1:1:1');
    final response = await http.get(url).timeout(Duration(milliseconds: 30));
    expect(response.statusCode, isNot(equals(200)));
    expect(() => throw Exception('Failed to load star data'), throwsException);
  }

  void testDataParsing() {
    Map<String, dynamic> json = {
      '0': 0.5,
      '1': 1.2,
      'Name': 'testStar',
      'magnitude': 3.4,
    };
    getStar testStar = getStar.fromJson(json);
    expect(testStar.x, 0.5);
    expect(testStar.y, 1.2);
    expect(testStar.name, 'testStar');
    expect(testStar.mag, 3.4);
    expect(testStar.length, 4);
  }

  void testDataPlotting() {
    List<ScatterSpot> spots = [
      ScatterSpot(0.5, 1.2,
          color: Color.fromARGB(255, 255, 255, 255), radius: 0.5),
      ScatterSpot(-0.7, 1, show: false),
      ScatterSpot(0.7, -1, show: false)
    ];
    expect(plottedData(spots, spots), isNotNull);
    expect(spots[0].x, 0.5);
    expect(spots[0].y, 1.2);
    expect(spots[0].color, Color.fromARGB(255, 255, 255, 255));
    expect(spots[0].radius, 0.5);
    expect(spots[1].show, false);
    expect(spots[2].show, false);
  }

  void testLabelsGeneration() {
    List<dynamic> labels = [];
    List<dynamic> a1 = ['star1', 'star2'];
    List<dynamic> a2 = ['planet1', 'planet2'];
    labels = a1 + a2;
    labels.add('Unknown');
    expect(labels, ['star1', 'star2', 'planet1', 'planet2', 'Unknown']);
  }
}
