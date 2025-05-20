import 'package:flutter_anim_app/models/user.dart';
import 'package:flutter_anim_app/services/api_service.dart';

class AuthService {
  final ApiService _apiService;

  AuthService({ApiService? apiService}) : _apiService = apiService ?? ApiService();

  Future<bool> login(String email, String password) async {
    try {
      final response = await _apiService.post(
        '/auth/token',
        {
          'username': email,
          'password': password,
        },
        requiresAuth: false,
      );

      if (response != null && response['access_token'] != null) {
        await _apiService.saveToken(response['access_token']);
        return true;
      }
      return false;
    } catch (e) {
      print('Login error: $e');
      return false;
    }
  }

  Future<void> logout() async {
    await _apiService.deleteToken();
  }

  Future<User?> getCurrentUser() async {
    try {
      final userData = await _apiService.get('/user/me');
      return User.fromJson(userData);
    } catch (e) {
      print('Get current user error: $e');
      return null;
    }
  }

  Future<User?> register(String name, String email, String password) async {
    try {
      final userData = await _apiService.post(
        '/user/',
        UserCreate(
          name: name,
          email: email,
          password: password,
        ).toJson(),
        requiresAuth: false,
      );
      return User.fromJson(userData);
    } catch (e) {
      print('Register error: $e');
      return null;
    }
  }

  Future<bool> isLoggedIn() async {
    final token = await _apiService.getToken();
    return token != null;
  }
}

