import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class ApiService {
  final String baseUrl = "http://192.168.1.81:5000";

  // 🔥 DETECTAR EMOCIÓN (MEJORADO)
  Future<Map<String, dynamic>> detectarEmocion(File imagen, String texto) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/emocion'),
      );

      // 📸 Imagen
      request.files.add(
        await http.MultipartFile.fromPath('file', imagen.path),
      );

      // 💬 Texto
      request.fields['texto'] = texto;

      var res = await request.send();
      var response = await http.Response.fromStream(res);

      // 🧪 DEBUG
      print("STATUS: ${response.statusCode}");
      print("BODY: ${response.body}");

      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return data;
      } else {
        return {
          "emocion": "error",
          "respuesta": "Error del servidor",
          "feedback": response.body
        };
      }
    } catch (e) {
      return {
        "emocion": "error",
        "respuesta": "No se pudo conectar",
        "feedback": e.toString()
      };
    }
  }

  // 📌 OBTENER PREGUNTA
  Future<Map<String, dynamic>> obtenerPregunta() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/pregunta"));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return {"pregunta": "Error al obtener pregunta"};
      }
    } catch (e) {
      return {"pregunta": "Sin conexión"};
    }
  }

  // ⏭ SIGUIENTE PREGUNTA
  Future<bool> siguientePregunta() async {
    try {
      final response = await http.post(Uri.parse("$baseUrl/siguiente"));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}