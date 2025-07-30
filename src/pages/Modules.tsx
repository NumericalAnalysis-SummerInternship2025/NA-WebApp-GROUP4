import React, { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookOpen, Calculator, BarChart3, Zap, Edit3, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useAuth } from '@/contexts/AuthContext';
import { Textarea } from "@/components/ui/textarea";
import { useSidebar } from "@/components/ui/sidebar";

// Minimal Module type matching backend
interface Module {
  id: number;
  titre: string;
  type: string;
  description?: string;
  contenu?: string;
  id_enseignant?: number;
  niveau?: string;
  categorie?: string;
  duree?: string;
  nb_lecons?: number;
  methodes?: string[];
  objectifs?: string[];
  enseignant_nom?: string;
}

// Add User type for enseignants
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface Lesson {
  id: number;
  titre: string;
  contenu: string;
  id_module: number;
}
interface Exercise {
  id: number;
  question: string;
  solution: string;
  id_module: number;
}

const typeIconMap: Record<string, any> = {
  "calculatrice": Calculator,
  "visualisation": BarChart3,
  "apprentissage": Zap,
  "": BookOpen,
};

const Modules: React.FC = () => {
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [form, setForm] = useState<Partial<Module>>({
    titre: "",
    type: "",
    description: "",
    contenu: "",
    id_enseignant: undefined,
    niveau: "Débutant",
    categorie: "",
    duree: "",
    nb_lecons: 1,
    methodes: [],
    objectifs: [],
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [enseignants, setEnseignants] = useState<User[]>([]);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();
  const [selectedModule, setSelectedModule] = useState<Module | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [showLessonModal, setShowLessonModal] = useState(false);
  const [lessonForm, setLessonForm] = useState<Partial<Lesson>>({ titre: '', contenu: '' });
  const [editingLessonId, setEditingLessonId] = useState<number | null>(null);
  const [showExerciseModal, setShowExerciseModal] = useState(false);
  const [exerciseForm, setExerciseForm] = useState<Partial<Exercise>>({ question: '', solution: '' });
  const [editingExerciseId, setEditingExerciseId] = useState<number | null>(null);
  const [editingModuleId, setEditingModuleId] = useState<number | null>(null);
  const [editData, setEditData] = useState<Partial<Module>>({});
  const { open } = useSidebar();


  useEffect(() => {
    fetchModules();
    fetchEnseignants();
  }, []);

  const fetchModules = () => {
    setLoading(true);
    fetch("http://localhost:8000/modules")
      .then((res) => res.json())
      .then((data) => {
        setModules(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Erreur lors du chargement des modules");
        setLoading(false);
      });
  };

  const fetchEnseignants = () => {
    fetch("http://localhost:8000/users")
      .then(res => res.json())
      .then(data => {
        const enseignantsList = data.filter(
          (u: User) => u.role && u.role.trim().toLowerCase() === "enseignant"
        );
        setEnseignants(enseignantsList);
      });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: name === "id_enseignant" ? Number(value) : value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.titre || !form.type || !user?.id) return;
    const method = editingId ? "PUT" : "POST";
    const url = editingId ? `http://localhost:8000/modules/${editingId}` : "http://localhost:8000/modules";
    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, id_enseignant: user.id }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Erreur lors de l'enregistrement");
        return res.json();
      })
      .then(() => {
        setForm({
          titre: "",
          type: "",
          description: "",
          contenu: "",
          id_enseignant: user?.id,
          niveau: "Débutant",
          categorie: "",
          duree: "",
          nb_lecons: 1,
          methodes: [],
          objectifs: [],
        });
        setEditingId(null);
        setShowModal(false);
        fetchModules();
      })
      .catch(() => setError("Erreur lors de l'enregistrement"));
  };

  const handleEdit = (mod: Module) => {
    setForm({
      titre: mod.titre,
      type: mod.type,
      description: mod.description,
      contenu: mod.contenu,
      id_enseignant: mod.id_enseignant,
      niveau: mod.niveau || "Débutant",
      categorie: mod.categorie || "",
      duree: mod.duree || "",
      nb_lecons: mod.nb_lecons || 1,
      methodes: mod.methodes || [],
      objectifs: mod.objectifs || [],
    });
    setEditingId(mod.id);
    setShowModal(true);
  };

  const handleDelete = (id: number) => {
    if (!window.confirm("Supprimer ce module ?")) return;
    fetch(`http://localhost:8000/modules/${id}`, { method: "DELETE" })
      .then(() => fetchModules())
      .catch(() => setError("Erreur lors de la suppression"));
  };

  const handleSaveModule = async (id: number) => {
    await fetch(`http://localhost:8000/modules/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editData)
    });
    setModules(modules.map(m => m.id === id ? { ...m, ...editData } : m));
    setEditingModuleId(null);
  };

  const filteredModules = modules.filter((mod) =>
    mod.titre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (mod.description || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Fetch lessons for selected module
  const fetchLessons = (moduleId: number) => {
    fetch(`http://localhost:8000/lessons/module/${moduleId}`)
      .then(res => res.json())
      .then(setLessons);
  };
  // Fetch exercises for selected module
  const fetchExercises = (moduleId: number) => {
    fetch(`http://localhost:8000/exercises/module/${moduleId}`)
      .then(res => res.json())
      .then(data => setExercises(data));
  };

  // Handlers for module click
  const handleModuleClick = (mod: Module) => {
    setSelectedModule(mod);
    fetchLessons(mod.id);
    fetchExercises(mod.id);
  };

  // CRUD for lessons
  const handleLessonSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!lessonForm.titre || !selectedModule) return;
    const method = editingLessonId ? 'PUT' : 'POST';
    const url = editingLessonId ? `http://localhost:8000/lessons/${editingLessonId}` : 'http://localhost:8000/lessons';
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...lessonForm, id_module: selectedModule.id }),
    })
      .then(res => res.json())
      .then(() => {
        setShowLessonModal(false);
        setEditingLessonId(null);
        setLessonForm({ titre: '', contenu: '' });
        fetchLessons(selectedModule.id);
      });
  };
  const handleEditLesson = (lesson: Lesson) => {
    setLessonForm({ titre: lesson.titre, contenu: lesson.contenu });
    setEditingLessonId(lesson.id);
    setShowLessonModal(true);
  };
  const handleDeleteLesson = (id: number) => {
    if (!window.confirm('Supprimer cette leçon ?')) return;
    fetch(`http://localhost:8000/lessons/${id}`, { method: 'DELETE' })
      .then(() => selectedModule && fetchLessons(selectedModule.id));
  };

  // CRUD for exercises
  const handleExerciseSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!exerciseForm.question || !selectedModule) return;
    const method = editingExerciseId ? 'PUT' : 'POST';
    const url = editingExerciseId ? `http://localhost:8000/exercises/${editingExerciseId}` : 'http://localhost:8000/exercises';
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...exerciseForm, id_module: selectedModule.id }),
    })
      .then(res => res.json())
      .then(() => {
        setShowExerciseModal(false);
        setEditingExerciseId(null);
        setExerciseForm({ question: '', solution: '' });
        fetchExercises(selectedModule.id);
      });
  };
  const handleEditExercise = (ex: Exercise) => {
    setExerciseForm({ question: ex.question, solution: ex.solution });
    setEditingExerciseId(ex.id);
    setShowExerciseModal(true);
  };
  const handleDeleteExercise = (id: number) => {
    if (!window.confirm('Supprimer cet exercice ?')) return;
    fetch(`http://localhost:8000/exercises/${id}`, { method: 'DELETE' })
      .then(() => selectedModule && fetchExercises(selectedModule.id));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <section className="container mx-auto px-4 py-12 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Modules d'Analyse Numérique
        </h1>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Explorez, créez et modifiez des modules interactifs pour maîtriser les concepts fondamentaux de l'analyse numérique.
        </p>
        {user?.role === "professeur" && (
          <div className="mb-8 flex justify-center">
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => navigate('/module-wizard')}>
              Ajouter un cours
            </Button>
          </div>
        )}
        <div className="max-w-md mx-auto mb-8">
          <Input
            placeholder="Rechercher un module..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full"
          />
        </div>
        {error && <div className="text-red-600 mb-4">{error}</div>}
      </section>
      <section className="container mx-auto px-4 pb-16">
        {loading ? (
          <div className="text-center">Chargement...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredModules.map((mod) => (
              <Card key={mod.id} className="flex flex-col bg-white shadow-lg border-0 rounded-lg overflow-hidden h-full">
                <div className="p-6 pb-4">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <BookOpen className="h-6 w-6 text-blue-600" />
                      <span className="px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        {mod.niveau || "Débutant"}
                      </span>
                    </div>
                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {mod.categorie || "Catégorie"}
                    </span>
                  </div>
                  
                  {editingModuleId === mod.id ? (
                    <div className="space-y-2">
                      <Input
                        value={editData.titre || ""}
                        onChange={e => setEditData({...editData, titre: e.target.value})}
                        placeholder="Titre"
                        className="font-bold"
                      />
                      <Textarea
                        value={editData.description || ""}
                        onChange={e => setEditData({...editData, description: e.target.value})}
                        placeholder="Description"
                      />
                      <Input
                        value={editData.type || ""}
                        onChange={e => setEditData({...editData, type: e.target.value})}
                        placeholder="Type"
                      />
                      <Input
                        value={editData.niveau || ""}
                        onChange={e => setEditData({...editData, niveau: e.target.value})}
                        placeholder="Niveau"
                      />
                      <Input
                        value={editData.categorie || ""}
                        onChange={e => setEditData({...editData, categorie: e.target.value})}
                        placeholder="Catégorie"
                      />
                      <Input
                        value={editData.duree || ""}
                        onChange={e => setEditData({...editData, duree: e.target.value})}
                        placeholder="Durée"
                      />
                      <Textarea
                        value={Array.isArray(editData.objectifs) ? editData.objectifs.join('\n') : ''}
                        onChange={e => setEditData({...editData, objectifs: e.target.value.split('\n').filter(line => line.trim() !== '')})}
                        placeholder="Un objectif par ligne"
                      />
                      <div className="flex gap-2 mt-2">
                        <Button onClick={() => handleSaveModule(mod.id)} className="bg-blue-600 text-white">Sauvegarder</Button>
                        <Button variant="outline" onClick={() => setEditingModuleId(null)}>Annuler</Button>
                      </div>
                    </div>
                  ) : (
                    <>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{mod.titre}</h3>
                      <p className="text-gray-600 text-sm leading-relaxed">{mod.description}</p>
                    </>
                  )}
                </div>

                {/* Duration and Lessons info with consistent alignment */}
                <div className="flex justify-between items-center mb-4 p-3 bg-gray-50 rounded-lg">
                  <div className="flex flex-col items-center">
                    <span className="font-bold text-lg text-blue-600">{mod.duree || "-"}</span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide">Durée</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <span className="font-bold text-lg text-blue-600">{mod.nb_lecons || 0}</span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide">Leçons</span>
                  </div>
                </div>

                {/* Content Section with flex-grow to push buttons to bottom */}
                <div className="flex-grow px-6">
                  {/* Learning objectives */}
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-800 mb-2 text-sm">Ce que vous apprendrez :</h4>
                    <ul className="list-disc list-inside text-green-700 text-sm space-y-1">
                      {Array.isArray(mod.objectifs) && mod.objectifs.length > 0 ? (
                        mod.objectifs.slice(0, 3).map((obj, i) => <li key={i}>{obj}</li>)
                      ) : (
                        <li>Objectif d'apprentissage à venir...</li>
                      )}
                    </ul>
                  </div>
                  
                  
                </div>

                {/* Button Section - Always at bottom with consistent layout */}
                <div className="p-6 pt-0 mt-auto">
                  {/* Primary Action Button - Always visible and prominent */}
                  <Button 
                    size="lg" 
                    className="w-full mb-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg shadow-md hover:shadow-lg transition-all duration-200" 
                    onClick={async () => {
                      // Fetch lessons for this module
                      const res = await fetch(`http://localhost:8000/lessons/module/${mod.id}`);
                      const lessons = await res.json();
                      if (lessons && lessons.length > 0) {
                        // Go to the first lesson's content page
                        navigate(`/module/${mod.id}`);
                      } else {
                        // Fallback: go to module overview
                        navigate(`/module/${mod.id}`);
                      }
                    }}
                  >
                    Commencer le module
                  </Button>
                  
                  {/* Professor name - Only shown to students */}
                  {user?.role === 'etudiant' && mod.enseignant_nom && (
                    <div className="mt-3 p-2 bg-blue-50 rounded-md border border-blue-100">
                      <div className="flex items-center justify-center text-sm text-blue-700">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        <span className="font-semibold">Professeur: </span>
                        <span className="ml-1">{mod.enseignant_nom}</span>
                      </div>
                    </div>
                  )}
                  
                  {/* Secondary Action Buttons - Icon buttons for edit/delete */}
                  <div className="flex gap-2 justify-center">
                    {user?.role === "professeur" && (
                      <>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className={`p-2 text-blue-700 border-blue-300 hover:bg-blue-50`}
                          onClick={() => {
                            setEditingModuleId(mod.id);
                            setEditData({
                              titre: mod.titre,
                              description: mod.description,
                              type: mod.type,
                              niveau: mod.niveau,
                              categorie: mod.categorie,
                              duree: mod.duree,
                              objectifs: mod.objectifs || [],
                            });
                          }}
                          title="Modifier"
                        >
                          <Edit3 className="h-4 w-4" />
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline"
                          className={`p-2 text-red-700 border-red-300 hover:bg-red-50`}
                          onClick={() => handleDelete(mod.id)}
                          title="Supprimer"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </>
                    )}
                  </div>
                  
                  {/* Role indicator for students */}
                  {user?.role !== "professeur" && (
                    <p className="text-xs text-gray-400 text-center mt-2 italic">
                      
                    </p>
                  )}
                </div>
              </Card>
            ))}
          </div>
        )}
        {filteredModules.length === 0 && !loading && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Aucun module trouvé pour "{searchTerm}"</p>
            <Button variant="outline" onClick={() => setSearchTerm("")} className="mt-4">
              Effacer la recherche
            </Button>
          </div>
        )}
        
        {/* Modal Dialog */}
        <Dialog open={showModal} onOpenChange={setShowModal}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>{editingId ? "Modifier le module" : "Ajouter un module"}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <Input name="titre" value={form.titre} onChange={handleChange} placeholder="Titre" required />
              <Input name="type" value={form.type} onChange={handleChange} placeholder="Type" required />
              <Input name="description" value={form.description} onChange={handleChange} placeholder="Description" />
              <Input name="contenu" value={form.contenu} onChange={handleChange} placeholder="Contenu" />
              <Input name="niveau" value={form.niveau || ''} onChange={handleChange} placeholder="Niveau (Débutant, Intermédiaire, Avancé)" />
              <Input name="categorie" value={form.categorie} onChange={handleChange} placeholder="Catégorie" />
              <Input name="duree" value={form.duree} onChange={handleChange} placeholder="Durée" />
              <textarea
                name="objectifs"
                value={Array.isArray(form.objectifs) ? form.objectifs.join('\n') : ''}
                onChange={e => setForm({ ...form, objectifs: e.target.value.split('\n').filter(line => line.trim() !== '') })}
                placeholder="Un objectif par ligne"
                rows={3}
                className="border rounded px-3 py-2 w-full"
              />
              <div className="flex gap-2 justify-end">
                <Button type="button" variant="outline" onClick={() => setShowModal(false)}>
                  Annuler
                </Button>
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white">
                  {editingId ? "Enregistrer" : "Ajouter"}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>

        {selectedModule && (
          <Dialog open={showLessonModal} onOpenChange={setShowLessonModal}>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>{editingLessonId ? "Modifier la leçon" : "Ajouter une leçon"}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleLessonSubmit} className="flex flex-col gap-4">
                <Input name="titre" value={lessonForm.titre || ''} onChange={e => setLessonForm({ ...lessonForm, titre: e.target.value })} placeholder="Titre de la leçon" required />
                <Textarea name="contenu" value={lessonForm.contenu || ''} onChange={e => setLessonForm({ ...lessonForm, contenu: e.target.value })} placeholder="Contenu" rows={4} />
                <div className="flex justify-end gap-2">
                  <Button variant="outline" onClick={() => setShowLessonModal(false)}>Annuler</Button>
                  <Button type="submit">{editingLessonId ? 'Sauvegarder' : 'Créer'}</Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        )}

        {selectedModule && (
          <Dialog open={showExerciseModal} onOpenChange={setShowExerciseModal}>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>{editingExerciseId ? "Modifier l'exercice" : "Ajouter un exercice"}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleExerciseSubmit} className="flex flex-col gap-4">
                <Input name="question" value={exerciseForm.question || ''} onChange={e => setExerciseForm({ ...exerciseForm, question: e.target.value })} placeholder="Question" required />
                <Textarea name="solution" value={exerciseForm.solution || ''} onChange={e => setExerciseForm({ ...exerciseForm, solution: e.target.value })} placeholder="Solution" rows={4} />
                <div className="flex justify-end gap-2">
                  <Button variant="outline" onClick={() => setShowExerciseModal(false)}>Annuler</Button>
                  <Button type="submit">{editingExerciseId ? 'Sauvegarder' : 'Créer'}</Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        )}

      </section>
    </div>
  );
};

export default Modules;