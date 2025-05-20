import 'package:flutter_anim_app/models/flock.dart';
import 'package:flutter_anim_app/services/api_service.dart';

class FlockService {
  final ApiService _apiService;

  FlockService({ApiService? apiService}) : _apiService = apiService ?? ApiService();

  Future<List<Flock>> getFlocks() async {
    try {
      final response = await _apiService.get('/flocks/');
      return (response as List).map((data) => Flock.fromJson(data)).toList();
    } catch (e) {
      print('Get flocks error: $e');
      return [];
    }
  }

  Future<Flock?> getFlock(int id) async {
    try {
      final response = await _apiService.get('/flocks/$id');
      return Flock.fromJson(response);
    } catch (e) {
      print('Get flock error: $e');
      return null;
    }
  }

  Future<Flock?> createFlock(String nom) async {
    try {
      final response = await _apiService.post(
        '/flocks/',
        {'nom': nom},
      );
      return Flock.fromJson(response);
    } catch (e) {
      print('Create flock error: $e');
      return null;
    }
  }

  Future<Flock?> updateFlock(int id, String nom) async {
    try {
      final response = await _apiService.put(
        '/flocks/$id',
        {'id': id, 'nom': nom},
      );
      return Flock.fromJson(response);
    } catch (e) {
      print('Update flock error: $e');
      return null;
    }
  }

  Future<bool> deleteFlock(int id) async {
    try {
      await _apiService.delete('/flocks/$id');
      return true;
    } catch (e) {
      print('Delete flock error: $e');
      return false;
    }
  }
}

