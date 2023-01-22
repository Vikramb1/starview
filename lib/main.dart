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

class getStar {
  final dynamic x;
  final dynamic y;
  final dynamic length;

  const getStar({
    required this.x,
    required this.y,
    required this.length,
  });

  factory getStar.fromJson(Map<String, dynamic> json) {
    return getStar(
      x: json['0'],
      y: json['1'],
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
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
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
  int duration = 15;
  getStar? data;
  List<double> arr = [1, 1, 1];
  List<ScatterSpot>? spots;

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
    // print(t.join(''))
    spots = plottedData(data);
  }

  List<ScatterSpot>? plottedData(var data) {
    if (data?.x.length > 5) {
      return List.generate(
          data?.x.length,
          (index) => ScatterSpot(
              data?.x.values.toList()[index], data?.y.values.toList()[index],
              color: Color.fromARGB(255, 255, 255, 255)));
    } else {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Card(
          //   color: Color.fromARGB(255, 0, 0, 0),
          //   child: Text(spots.toString(), style: TextStyle(color: Colors.white)),
          // )
          color: Color.fromARGB(255, 0, 0, 0),
          child: ScatterChart(ScatterChartData(
            scatterSpots: spots,
            borderData: FlBorderData(
              show: false,
            ),
            gridData: FlGridData(
              show: false,
            ),
            titlesData: FlTitlesData(
              show: false,
            ),
          ))),
    );
  }
}
