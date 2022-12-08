import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
// import 'package:sensors_plus/sensors_plus.dart';
import 'package:motion_sensors/motion_sensors.dart';
import 'package:vector_math/vector_math_64.dart' hide Colors;
import 'dart:convert';
import 'dart:async';

Future<getPlanet> fetchPlanet() async {
  final response = await http.get(Uri.parse('http://127.0.0.1:5000/planets'));
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return getPlanet.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load planet data');
  }
}

Future<getStar> fetchStar() async {
  final response = await http.get(Uri.parse('http://127.0.0.1:5000/stars'));

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

class getPlanet {
  final dynamic dec;
  final dynamic ra;

  const getPlanet({
    required this.dec,
    required this.ra,
  });

  factory getPlanet.fromJson(Map<String, dynamic> json) {
    return getPlanet(
      dec: json['dec'],
      ra: json['ra'],
    );
  }
}

class getStar {
  final dynamic x;
  final dynamic y;

  const getStar({
    required this.x,
    required this.y,
  });

  factory getStar.fromJson(Map<String, dynamic> json) {
    return getStar(
      x: json['x'],
      y: json['y'],
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
  int duration = 1;

  @override
  void initState() {
    super.initState();
    // Timer.periodic(Duration(seconds: duration), (Timer t) => _getOrientation());
    motionSensors.absoluteOrientation.listen((AbsoluteOrientationEvent event) {
      setState(() {
        _absoluteOrientation.setValues(event.yaw, event.pitch, event.roll);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                Text(_absoluteOrientation.x.toStringAsFixed(4),
                    style: TextStyle(fontSize: 25)),
                Text(_absoluteOrientation.y.toStringAsFixed(4),
                    style: TextStyle(fontSize: 25)),
                Text(_absoluteOrientation.z.toStringAsFixed(4),
                    style: TextStyle(fontSize: 25)),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
