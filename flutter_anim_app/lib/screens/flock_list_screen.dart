import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_anim_app/models/flock.dart';
import 'package:flutter_anim_app/providers/flock_provider.dart';
import 'package:flutter_anim_app/screens/flock_detail_screen.dart';

class FlockListScreen extends StatefulWidget {
  const FlockListScreen({Key? key}) : super(key: key);

  @override
  _FlockListScreenState createState() => _FlockListScreenState();
}

class _FlockListScreenState extends State<FlockListScreen> {
  final _formKey = GlobalKey<FormState>();
  final _flockNameController = TextEditingController();

  @override
  void dispose() {
    _flockNameController.dispose();
    super.dispose();
  }

  Future<void> _refreshFlocks() async {
    await Provider.of<FlockProvider>(context, listen: false).loadFlocks();
  }

  void _showAddFlockDialog() {
    _flockNameController.clear();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Ajouter un troupeau'),
        content: Form(
          key: _formKey,
          child: TextFormField(
            controller: _flockNameController,
            decoration: const InputDecoration(
              labelText: 'Nom du troupeau',
              border: OutlineInputBorder(),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Veuillez entrer un nom';
              }
              return null;
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Annuler'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (_formKey.currentState!.validate()) {
                final flockProvider = Provider.of<FlockProvider>(context, listen: false);
                final success = await flockProvider.createFlock(_flockNameController.text.trim());
                if (success && mounted) {
                  Navigator.of(context).pop();
                }
              }
            },
            child: const Text('Ajouter'),
          ),
        ],
      ),
    );
  }

  void _showEditFlockDialog(Flock flock) {
    _flockNameController.text = flock.nom;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Modifier le troupeau'),
        content: Form(
          key: _formKey,
          child: TextFormField(
            controller: _flockNameController,
            decoration: const InputDecoration(
              labelText: 'Nom du troupeau',
              border: OutlineInputBorder(),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Veuillez entrer un nom';
              }
              return null;
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Annuler'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (_formKey.currentState!.validate()) {
                final flockProvider = Provider.of<FlockProvider>(context, listen: false);
                final success = await flockProvider.updateFlock(
                  flock.id!,
                  _flockNameController.text.trim(),
                );
                if (success && mounted) {
                  Navigator.of(context).pop();
                }
              }
            },
            child: const Text('Enregistrer'),
          ),
        ],
      ),
    );
  }

  void _confirmDeleteFlock(Flock flock) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Supprimer le troupeau'),
        content: Text('Êtes-vous sûr de vouloir supprimer le troupeau "${flock.nom}" ?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Annuler'),
          ),
          ElevatedButton(
            onPressed: () async {
              final flockProvider = Provider.of<FlockProvider>(context, listen: false);
              final success = await flockProvider.deleteFlock(flock.id!);
              if (success && mounted) {
                Navigator.of(context).pop();
              }
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Supprimer'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Consumer<FlockProvider>(
        builder: (context, flockProvider, child) {
          if (flockProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (flockProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Erreur: ${flockProvider.error}',
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _refreshFlocks,
                    child: const Text('Réessayer'),
                  ),
                ],
              ),
            );
          }

          if (flockProvider.flocks.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'Aucun troupeau trouvé',
                    style: TextStyle(fontSize: 18),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _showAddFlockDialog,
                    child: const Text('Ajouter un troupeau'),
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: _refreshFlocks,
            child: ListView.builder(
              itemCount: flockProvider.flocks.length,
              itemBuilder: (context, index) {
                final flock = flockProvider.flocks[index];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: ListTile(
                    title: Text(
                      flock.nom,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text('ID: ${flock.id}'),
                    leading: const CircleAvatar(
                      child: Icon(Icons.pets),
                    ),
                    trailing: PopupMenuButton(
                      itemBuilder: (context) => [
                        const PopupMenuItem(
                          value: 'edit',
                          child: Row(
                            children: [
                              Icon(Icons.edit, size: 18),
                              SizedBox(width: 8),
                              Text('Modifier'),
                            ],
                          ),
                        ),
                        const PopupMenuItem(
                          value: 'delete',
                          child: Row(
                            children: [
                              Icon(Icons.delete, size: 18, color: Colors.red),
                              SizedBox(width: 8),
                              Text('Supprimer', style: TextStyle(color: Colors.red)),
                            ],
                          ),
                        ),
                      ],
                      onSelected: (value) {
                        if (value == 'edit') {
                          _showEditFlockDialog(flock);
                        } else if (value == 'delete') {
                          _confirmDeleteFlock(flock);
                        }
                      },
                    ),
                    onTap: () async {
                      await flockProvider.selectFlock(flock.id!);
                      if (mounted) {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => FlockDetailScreen(flock: flock),
                          ),
                        );
                      }
                    },
                  ),
                );
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddFlockDialog,
        tooltip: 'Ajouter un troupeau',
        child: const Icon(Icons.add),
      ),
    );
  }
}

