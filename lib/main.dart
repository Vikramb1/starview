// import 'dart:ffi';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:motion_sensors/motion_sensors.dart';
import 'package:vector_math/vector_math_64.dart' hide Colors;
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'dart:async';

Future<getStar> fetchStar(String normal) async {
  final url = Uri.parse('http://10.0.2.2:5000/stars?normal=' + normal);
  final Map<String, String> httpHeaders = {
    // "Connection": "Keep-Alive",
    // "Keep-Alive": "timeout=1, max=1"
  };
  final response = await http
      .get(url, headers: httpHeaders)
      .timeout(Duration(milliseconds: 30));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return getStar.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load star data');
  }
}

Future<getPlanet> fetchPlanet(String normal) async {
  final url = Uri.parse('http://10.0.2.2:5000/planets?normal=' + normal);
  final Map<String, String> httpHeaders = {
    // "Connection": "Keep-Alive",
    // "Keep-Alive": "timeout=1, max=1"
  };
  final response = await http
      .get(url, headers: httpHeaders)
      .timeout(Duration(milliseconds: 30));
  // final response = await http
  //     .get(Uri.parse('http://10.0.2.2:5000/planets?normal=' + normal));
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return getPlanet.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load star data');
  }
}

class getStar {
  final dynamic x;
  final dynamic y;
  final dynamic name;
  final dynamic mag;
  final dynamic length;

  const getStar({
    required this.x,
    required this.y,
    required this.name,
    required this.mag,
    required this.length,
  });

  factory getStar.fromJson(Map<String, dynamic> json) {
    return getStar(
      x: json['0'],
      y: json['1'],
      name: json['Name'],
      mag: json['magnitude'],
      length: json.length,
    );
  }
}

class getPlanet {
  final dynamic x;
  final dynamic y;
  final dynamic name;
  final dynamic length;

  const getPlanet({
    required this.x,
    required this.y,
    required this.name,
    required this.length,
  });

  factory getPlanet.fromJson(Map<String, dynamic> json) {
    return getPlanet(
      x: json['0'],
      y: json['1'],
      name: json['Name'],
      length: json.length,
    );
  }
}

void main() {
  print('starting up....');
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'StarView',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'StarView'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Vector3 _absoluteOrientation = Vector3.zero();
  int duration = 100;
  getStar? data;
  List<double> arr = [1, 1, 1];
  List<ScatterSpot>? spots;
  List<int> selected_spots = [];
  List<dynamic> labels = [];
  String value = '';

  @override
  void initState() {
    super.initState();
    Timer.periodic(Duration(milliseconds: duration), (Timer t) => getData());
  }

  void getData() async {
    motionSensors.absoluteOrientation.listen((AbsoluteOrientationEvent event) {
      setState(() {
        _absoluteOrientation.setValues(event.yaw, event.pitch, event.roll);
      });
    });
    _absoluteOrientation.copyIntoArray(arr, 0);
    List<String> t = arr.map((el) => el.toString()).toList();
    getStar data = await fetchStar(t.join(':'));
    getPlanet data2 = await fetchPlanet(t.join(':'));
    spots = plottedData(data, data2);
    // print('called');
  }

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
              color:
                  planetsCol[data2?.name.values.toList()[index].toLowerCase()],
              radius:
                  planetsSize[data2.name.values.toList()[index].toLowerCase()]
                      ?.toDouble(),
              show: true));
      List<dynamic> a1 = data?.name.values.toList();
      List<dynamic> a2 = data2?.name.values.toList();
      labels = a1 + a2;
      labels.add('Unknown');
      List<ScatterSpot> combined = m + p;
      return combined;
    } else {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
        aspectRatio: 1,
        child: Card(
          color: Color.fromARGB(255, 0, 0, 0),
          child: ScatterChart(
            ScatterChartData(
                scatterSpots: spots,
                borderData: FlBorderData(
                  show: false,
                ),
                gridData: FlGridData(
                  show: false,
                ),
                maxX: 0.7,
                minX: -0.7,
                minY: -1,
                maxY: 1,
                titlesData: FlTitlesData(
                  show: false,
                ),
                showingTooltipIndicators: selected_spots,
                scatterTouchData: ScatterTouchData(
                    enabled: true,
                    handleBuiltInTouches: false,
                    mouseCursorResolver: (FlTouchEvent touchEvent,
                        ScatterTouchResponse? response) {
                      return response == null || response.touchedSpot == null
                          ? MouseCursor.defer
                          : SystemMouseCursors.click;
                    },
                    touchTooltipData: ScatterTouchTooltipData(
                      tooltipBgColor: Color.fromARGB(255, 184, 174, 174),
                      getTooltipItems: (ScatterSpot touchedBarSpot) {
                        int? nme = spots
                            ?.where((z) => (z.x - touchedBarSpot.x).abs() == 0)
                            .map((z) => spots?.indexOf(z))
                            .toList()[0];
                        int ind = nme ?? labels.length - 1;
                        value = labels[ind];
                        selected_spots = [];
                        return ScatterTooltipItem(
                          value,
                          textStyle: TextStyle(
                            height: 1.2,
                            color: Colors.grey[100],
                            fontStyle: FontStyle.italic,
                          ),
                        );
                      },
                    ),
                    touchCallback: (FlTouchEvent event,
                        ScatterTouchResponse? touchResponse) {
                      if (touchResponse == null ||
                          touchResponse.touchedSpot == null) {
                        return;
                      }
                      if (event is FlTapUpEvent) {
                        final sectionIndex =
                            touchResponse.touchedSpot!.spotIndex;
                        setState(() {
                          if (selected_spots.contains(sectionIndex)) {
                            selected_spots.remove(sectionIndex);
                          } else {
                            selected_spots.add(sectionIndex);
                          }
                        });
                      }
                    })),
            swapAnimationDuration: Duration(milliseconds: 1),
          ),
        ));
    // );
  }
}
