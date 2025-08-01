import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar } from '@/components/ui/calendar';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Bell, BookOpen, Users, BarChart3, Calendar as CalendarIcon, FileText, PlusCircle, CheckCircle, AlertTriangle, Trash2, Loader2, RefreshCw } from 'lucide-react';
import { StudentSuccessRates, mockStudentSuccessData } from '@/components/dashboard/StudentSuccessRates';
import { useAuth } from '@/contexts/AuthContext';

// --- Types ---
interface CalendarEvent {
  id: number;
  title: string;
  date: string;
  type: 'exam' | 'assignment' | 'reminder';
  id_enseignant: number;
}

interface ModuleSuccess {
  id_module: number;
  name: string;
  successRate: number;
}

interface DashboardStats {
  totalStudents: number;
  activeModules: number;
  averageSuccessRate: number;
  assignmentsToGrade: number;
  moduleSuccess: ModuleSuccess[];
}

// --- Main Component ---
export default function ProfessorDashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showEventDialog, setShowEventDialog] = useState(false);
  const [newEvent, setNewEvent] = useState({ title: '', date: '', type: 'reminder' as CalendarEvent['type'] });

  const fetchData = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);
    try {
      // Fetch stats and events in parallel
      const [statsResponse, eventsResponse] = await Promise.all([
        fetch(`http://localhost:8000/api/dashboard/stats/${user.id}`),
        fetch(`http://localhost:8000/api/events/${user.id}`)
      ]);

      if (!statsResponse.ok) throw new Error('Failed to fetch dashboard stats');
      if (!eventsResponse.ok) throw new Error('Failed to fetch events');

      const statsData = await statsResponse.json();
      const eventsData = await eventsResponse.json();

      setStats(statsData);
      setEvents(eventsData);

    } catch (error) {
      console.error(error);
      // You might want to set an error state here to show in the UI
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSaveEvent = async () => {
    if (!user || !newEvent.title || !newEvent.date) {
      alert("Le titre et la date sont obligatoires.");
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...newEvent, id_enseignant: user.id }),
      });
      if (!response.ok) throw new Error('Failed to save event');
      await fetchData(); // Refetch all data
      setShowEventDialog(false);
      setNewEvent({ title: '', date: '', type: 'reminder' });
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteEvent = async (eventId: number) => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cet événement ?")) return;

    try {
      const response = await fetch(`http://localhost:8000/api/events/${eventId}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete event');
      setEvents(prevEvents => prevEvents.filter(event => event.id !== eventId));
    } catch (error) {
      console.error(error);
    }
  };

  const StatCard = ({ title, value, icon, description, isLoading }: { title: string, value: string | number, icon: React.ReactNode, description: string, isLoading?: boolean }) => (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        ) : (
          <>
            <div className="text-2xl font-bold">{value}</div>
            <p className="text-xs text-muted-foreground">{description}</p>
          </>
        )}
      </CardContent>
    </Card>
  );

  return (
    <ScrollArea className="h-full">
      <div className="container mx-auto p-4 md:p-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Tableau de Bord Professeur</h1>
            <p className="text-muted-foreground">Bienvenue, {user?.name || 'Professeur'} ! Voici un aperçu de vos cours.</p>
          </div>
          <Button variant="outline" size="sm" onClick={fetchData} disabled={isLoading}>
            {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <RefreshCw className="mr-2 h-4 w-4" />}
            Rafraîchir
          </Button>
        </div>

        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
            
            <TabsTrigger value="calendar">Calendrier & Tâches</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <StatCard isLoading={isLoading} title="Total d'Étudiants" value={stats?.totalStudents ?? 0} icon={<Users className="h-4 w-4 text-muted-foreground" />} description="Dans toutes vos classes" />
              <StatCard isLoading={isLoading} title="Modules Actifs" value={stats?.activeModules ?? 0} icon={<BookOpen className="h-4 w-4 text-muted-foreground" />} description="Modules avec activité récente" />
              <StatCard isLoading={isLoading} title="Taux de Réussite Moyen" value={`${stats?.averageSuccessRate.toFixed(2) ?? 0}%`} icon={<CheckCircle className="h-4 w-4 text-muted-foreground" />} description="Basé sur les derniers quiz" />
              <StatCard isLoading={isLoading} title="Devoirs à Corriger" value={stats?.assignmentsToGrade ?? 0} icon={<FileText className="h-4 w-4 text-muted-foreground" />} description="En attente de votre évaluation" />
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
              <Card className="lg:col-span-4">
                <CardHeader>
                  <CardTitle>Progression Globale par Module</CardTitle>
                  <CardDescription>Taux de réussite moyen pour chaque module actif.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full"><Loader2 className="h-8 w-8 animate-spin text-muted-foreground" /></div>
                  ) : (
                    stats?.moduleSuccess.map(module => (
                      <div key={module.id_module} className="space-y-1">
                        <div className="flex justify-between items-center">
                          <p className="text-sm font-medium">{module.name}</p>
                          <p className="text-sm text-muted-foreground">{module.successRate.toFixed(2)}%</p>
                        </div>
                        <Progress value={module.successRate} />
                      </div>
                    ))
                  )}
                </CardContent>
              </Card>
              <Card className="lg:col-span-3">
                <CardHeader>
                  <CardTitle>Alertes et Notifications</CardTitle>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-48">
                    <div className="space-y-4">
                       <div className="flex items-start gap-3">
                          <div className="mt-1">
                            <AlertTriangle className="h-4 w-4 text-yellow-500" />
                          </div>
                          <p className="text-sm text-muted-foreground">{stats?.assignmentsToGrade ?? 0} devoirs en attente de correction.</p>
                        </div>
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Progress Tab */}
          <TabsContent value="progress" className="space-y-4">
            <StudentSuccessRates data={mockStudentSuccessData} />
          </TabsContent>

          {/* Calendar Tab */}
          <TabsContent value="calendar" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Calendrier et Événements</CardTitle>
                <CardDescription>Gérez vos échéances, examens et rappels.</CardDescription>
              </CardHeader>
              <CardContent className="grid gap-8 md:grid-cols-2">
                <div>
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={setDate}
                    className="rounded-md border"
                  />
                </div>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-semibold">Événements à venir</h3>
                    <Dialog open={showEventDialog} onOpenChange={setShowEventDialog}>
                      <DialogTrigger asChild>
                        <Button size="sm" disabled={!user}>
                          <PlusCircle className="mr-2 h-4 w-4" />
                          Ajouter un événement
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Créer un nouvel événement</DialogTitle>
                          <DialogDescription>
                            Ajoutez un examen, un devoir ou un rappel à votre calendrier.
                          </DialogDescription>
                        </DialogHeader>
                        <div className="space-y-4 py-4">
                           <div className="space-y-2">
                            <Label htmlFor="event-title">Titre</Label>
                            <Input id="event-title" value={newEvent.title} onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })} placeholder="Ex: Examen Final" />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="event-date">Date</Label>
                            <Input id="event-date" type="date" value={newEvent.date} onChange={(e) => setNewEvent({ ...newEvent, date: e.target.value })} />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="event-type">Type</Label>
                             <Select value={newEvent.type} onValueChange={(value: CalendarEvent['type']) => setNewEvent({ ...newEvent, type: value })}>
                              <SelectTrigger>
                                <SelectValue placeholder="Sélectionner un type" />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="exam">Examen</SelectItem>
                                <SelectItem value="assignment">Devoir</SelectItem>
                                <SelectItem value="reminder">Rappel</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                        </div>
                        <DialogFooter>
                          <Button variant="outline" onClick={() => setShowEventDialog(false)}>Annuler</Button>
                          <Button onClick={handleSaveEvent}>Sauvegarder</Button>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  </div>
                  <ScrollArea className="h-72">
                    {isLoading ? (
                      <div className="flex items-center justify-center h-full">
                        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                      </div>
                    ) : (
                      <div className="space-y-3 pr-4">
                        {events.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()).map(event => (
                          <div key={event.id} className="flex items-center gap-4 p-3 rounded-lg border bg-background">
                            <CalendarIcon className="h-5 w-5 text-muted-foreground" />
                            <div className="flex-grow">
                              <p className="font-medium">{event.title}</p>
                              <p className="text-sm text-muted-foreground">{new Date(event.date).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
                            </div>
                            <Badge variant={event.type === 'exam' ? 'destructive' : 'secondary'}>{event.type}</Badge>
                            <Button variant="ghost" size="icon" onClick={() => handleDeleteEvent(event.id)}>
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                      </div>
                    )}
                  </ScrollArea>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </ScrollArea>
  );
}
