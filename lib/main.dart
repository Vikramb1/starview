// import 'dart:ffi';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:motion_sensors/motion_sensors.dart';
import 'package:vector_math/vector_math_64.dart' hide Colors;
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'dart:async';

Future<getStar> fetchStar(String normal) async {
  final response = await http.get(
      Uri.parse('http://10.0.2.2:5000/stars?normal=' + normal),
      headers: {"Keep-Alive": "timeout=5, max=1"});
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
  final response = await http.get(
      Uri.parse('http://10.0.2.2:5000/planets?normal=' + normal),
      headers: {"Keep-Alive": "timeout=5, max=1"});
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
      title: 'Flutter Demo',
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
  int duration = 250;
  getStar? data;
  List<double> arr = [1, 1, 1];
  List<ScatterSpot>? spots;
  List<int> selected_spots = [];
  List<String> labels = [];
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
  }

  List<ScatterSpot>? plottedData(var data, var data2) {
    if (data?.x.length > 5) {
      List<ScatterSpot> m = List.generate(
          data?.x.length,
          (index) => ScatterSpot(
              data?.x.values.toList()[index], data?.y.values.toList()[index],
              color: Color.fromARGB(255, 255, 255, 255),
              radius: (4 - data?.mag.values.toList()[index]).toDouble()));
      m.add(ScatterSpot(-0.7, 1, show: false));
      m.add(ScatterSpot(0.7, -1, show: false));
      List<Color> planet_cols = [
        // Color.fromARGB(255, 255, 255, 255),
        // Color.fromARGB(255, 255, 255, 255),
        // Color.fromARGB(255, 255, 255, 255),
        // Color.fromARGB(255, 255, 255, 255),
        // Color.fromARGB(255, 255, 255, 255),
        // Color.fromARGB(255, 255, 255, 255),
        // Color.fromARGB(255, 255, 255, 255),
        Color.fromARGB(255, 219, 206, 202),
        Color.fromARGB(255, 165, 124, 27),
        Color.fromARGB(255, 69, 24, 4),
        Color.fromARGB(255, 188, 175, 178),
        Color.fromRGBO(234, 214, 184, 1),
        Color.fromARGB(255, 209, 231, 231),
        Color.fromARGB(255, 75, 112, 221),
        Color.fromARGB(255, 254, 252, 215)
      ];
      List<double> sizes = [10, 13, 13, 20, 18, 15, 15, 23];
      // List<ScatterSpot> m = List.generate(
      //     data?.x.length,
      //     (index) => ScatterSpot(
      //         data?.x.values.toList()[index], data?.y.values.toList()[index],
      //         color: Color.fromARGB(255, 255, 255, 255),
      //         radius: (4 - data?.mag.values.toList()[index]).toDouble()));
      List<ScatterSpot> p = List.generate(
          data2?.x.length,
          (index) => ScatterSpot(
              data2?.x.values.toList()[index], data2?.y.values.toList()[index],
              color: planet_cols[index], radius: sizes[index], show: true));
      // List<ScatterSpot> p = [
      //   ScatterSpot(0, 0, color: Color.fromARGB(255, 255, 255, 255), radius: 10)
      // ];
      labels = data?.name.values.toList() + data2?.name.values.toList();
      List<ScatterSpot> combined = m + p;
      // print(combined.length);
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
          //   color: Color.fromARGB(255, 0, 0, 0),
          //   child: Text(spots.toString(), style: TextStyle(color: Colors.white)),
          // )
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
              // showingTooltipIndicators: selected_spots,
              // scatterTouchData: ScatterTouchData(
              //     enabled: true,
              //     handleBuiltInTouches: false,
              //     mouseCursorResolver: (FlTouchEvent touchEvent,
              //         ScatterTouchResponse? response) {
              //       return response == null || response.touchedSpot == null
              //           ? MouseCursor.defer
              //           : SystemMouseCursors.click;
              //     },
              //     touchTooltipData: ScatterTouchTooltipData(
              //       tooltipBgColor: Color.fromARGB(255, 255, 0, 0),
              //       getTooltipItems: (ScatterSpot touchedBarSpot) {
              //         print('here');
              //         var nme = spots
              //             ?.where((z) => z.x == touchedBarSpot.x)
              //             .map((z) => spots?.indexOf(z))
              //             .toList()[0];
              //         if (nme == null) {
              //           value = '';
              //         } else {
              //           value = labels[nme];
              //         }
              //         return ScatterTooltipItem(
              //           value,
              //           textStyle: TextStyle(
              //             height: 1.2,
              //             color: Colors.grey[100],
              //             fontStyle: FontStyle.italic,
              //           ),
              //           //   bottomMargin: 10,
              //           //   children: [
              //           //     TextSpan(
              //           //       text: '${touchedBarSpot.x.toInt()} \n',
              //           //       style: const TextStyle(
              //           //         color: Colors.white,
              //           //         fontStyle: FontStyle.normal,
              //           //         fontWeight: FontWeight.bold,
              //           //       ),
              //           //     ),
              //           //     TextSpan(
              //           //       text: 'Y: ',
              //           //       style: TextStyle(
              //           //         height: 1.2,
              //           //         color: Colors.grey[100],
              //           //         fontStyle: FontStyle.italic,
              //           //       ),
              //           //     ),
              //           // TextSpan(
              //           //   text: touchedBarSpot.y.toInt().toString(),
              //           //   style: const TextStyle(
              //           //     color: Colors.white,
              //           //     fontStyle: FontStyle.normal,
              //           //     fontWeight: FontWeight.bold,
              //           //   ),
              //           // ),
              //         );
              //       },
              //     ),
              //     touchCallback: (FlTouchEvent event,
              //         ScatterTouchResponse? touchResponse) {
              //       if (touchResponse == null ||
              //           touchResponse.touchedSpot == null) {
              //         return;
              //       }
              //       if (event is FlTapUpEvent) {
              //         final sectionIndex =
              //             touchResponse.touchedSpot!.spotIndex;
              //         setState(() {
              //           if (selected_spots.contains(sectionIndex)) {
              //             selected_spots.remove(sectionIndex);
              //           } else {
              //             selected_spots.add(sectionIndex);
              //           }
              //         });
              //       }
              // })),
            ),
            swapAnimationDuration: Duration(milliseconds: 0),
          )),
    );
  }
}
