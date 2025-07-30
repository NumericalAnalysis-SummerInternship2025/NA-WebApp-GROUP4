import React, { useState, useEffect, useRef } from 'react';
import JXG from 'jsxgraph';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { toast } from '@/hooks/use-toast';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { useAuth } from '@/contexts/AuthContext';

type HistoryEntry = {
  id: number;
  equation1: string;
  equation2: string;
  solution_type: string;
  solution: { x: number; y: number } | null;
};

const LinearSystemSolver = () => {
  const { user } = useAuth();
  const boardContainerRef = useRef<HTMLDivElement>(null);
  const boardRef = useRef<JXG.Board | null>(null);
  const [eq1, setEq1] = useState('y = 2x + 1');
  const [eq2, setEq2] = useState('y = -x + 4');
  const [solution, setSolution] = useState<{ x: number; y: number } | null>(null);
  const [solutionType, setSolutionType] = useState('unique');
  const [coeffs, setCoeffs] = useState<{ c1: any; c2: any }>({ c1: null, c2: null });
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  const solveSystem = async () => {
    if (!eq1 || !eq2) return;
    try {
      const response = await axios.post('http://localhost:8000/api/solve-linear-system', {
        eq1,
        eq2,
        user_id: user?.id,
      });
      const { solution, solution_type, coeffs1, coeffs2 } = response.data;
      setSolution(solution);
      setSolutionType(solution_type);
      setCoeffs({ c1: coeffs1, c2: coeffs2 });

      if (user && solution_type !== 'invalid') {
        fetchHistory();
      }
    } catch (error) {
      console.error("Error solving system:", error);
      toast({ variant: 'destructive', title: 'Erreur du serveur', description: 'Impossible de contacter le backend.' });
    }
  };

  const fetchHistory = async () => {
    if (!user) return;
    try {
      const response = await axios.get(`http://localhost:8000/api/history/linear-system/${user.id}`);
      const formattedHistory = response.data.map((item: any) => ({
        ...item,
        solution: item.solution_x !== null ? { x: item.solution_x, y: item.solution_y } : null,
      }));
      setHistory(formattedHistory);
    } catch (error) {
      console.error("Failed to fetch history:", error);
      toast({ variant: 'destructive', title: 'Erreur', description: 'Impossible de charger l\'historique.' });
    }
  };

  useEffect(() => {
    if (user) {
      fetchHistory();
    }
  }, [user]);

  useEffect(() => {
    solveSystem(); // Solve on initial load
  }, []);

  useEffect(() => {
    if (!boardContainerRef.current) return;

    const board = JXG.JSXGraph.initBoard(boardContainerRef.current, {
      boundingbox: [-10, 10, 10, -10],
      axis: true,
      grid: true,
      showCopyright: false,
      showNavigation: true,
    });
    boardRef.current = board;

    const updateLineEquation = (line, setEq) => {
        const slope = line.getSlope();
        const yIntercept = line.getRise();
        const sign = yIntercept < 0 ? '-' : '+';
        const eq = `y = ${slope.toFixed(2)}x ${sign} ${Math.abs(yIntercept).toFixed(2)}`;
        setEq(eq);
    };

    // Define lines by two invisible, draggable points
    const p1 = board.create('point', [-5, -5], { visible: false });
    const p2 = board.create('point', [5, 5], { visible: false });
    const line1 = board.create('line', [p1, p2], { strokeColor: '#3b82f6', strokeWidth: 2, fixed: false });

    const p3 = board.create('point', [-5, 5], { visible: false });
    const p4 = board.create('point', [5, -5], { visible: false });
    const line2 = board.create('line', [p3, p4], { strokeColor: '#ef4444', strokeWidth: 2, fixed: false });

    const intersection = board.create('intersection', [line1, line2, 0], {
        name: 'Solution',
        face: 'o',
        size: 4,
        fillColor: '#10b981',
        strokeColor: '#10b981',
        visible: true
    });

    const updateAll = () => {
        updateLineEquation(line1, setEq1);
        updateLineEquation(line2, setEq2);
        if (intersection.coords.usrCoords[1] !== Infinity) {
            setSolution({ x: intersection.coords.usrCoords[1], y: intersection.coords.usrCoords[2] });
            setSolutionType('unique');
        } else {
            setSolution(null);
            setSolutionType('none');
        }
    };

    // Listen to the 'drag' event on the lines themselves
    line1.on('drag', updateAll);
    line2.on('drag', updateAll);

    // Initial update
    updateAll();

    // Cleanup
    return () => {
      if (boardRef.current) {
        JXG.JSXGraph.freeBoard(boardRef.current);
        boardRef.current = null;
      }
    };
  }, []);

  const handleClearHistory = async () => {
    if (!user) return;
    try {
      await axios.delete(`http://localhost:8000/api/history/linear-system/${user.id}`);
      setHistory([]);
      toast({ title: 'Succès', description: 'Votre historique a été vidé.' });
    } catch (error) {
      console.error("Failed to clear history:", error);
      toast({ variant: 'destructive', title: 'Erreur', description: 'Impossible de vider l\'historique.' });
    }
  };

  const getSolutionText = () => {
    switch (solutionType) {
      case 'unique':
        return solution ? `Solution unique : (${solution.x.toFixed(2)}, ${solution.y.toFixed(2)})` : '';
      case 'none':
        return 'Aucune solution (lignes parallèles).';
      case 'infinite':
        return 'Une infinité de solutions (lignes confondues).';
      case 'invalid':
        return 'Format d\'équation invalide. Utilisez y = mx + b.';
      default:
        return '';
    }
  };

  return (
    <div className="p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Solveur de Système d'Équations Linéaires</CardTitle>
            <CardDescription>Entrez deux équations pour visualiser la solution.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <Label htmlFor="eq1">Équation 1 (y = mx + b)</Label>
                <Input id="eq1" value={eq1} onChange={(e) => setEq1(e.target.value)} />
              </div>
              <div>
                <Label htmlFor="eq2">Équation 2 (y = mx + b)</Label>
                <Input id="eq2" value={eq2} onChange={(e) => setEq2(e.target.value)} />
              </div>
              <Button onClick={solveSystem}>Résoudre</Button>
              <div className="font-bold text-lg">{getSolutionText()}</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Visualisation Graphique</CardTitle>
          </CardHeader>
          <CardContent>
            <div ref={boardContainerRef} className="jxgbox" style={{ width: '100%', height: '400px' }}></div>
          </CardContent>
        </Card>
      </div>

      {user && history.length > 0 && (
        <Card className="mt-8">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Historique des essais</CardTitle>
              <CardDescription>Voici la liste des systèmes que vous avez testés.</CardDescription>
            </div>
            <Button onClick={handleClearHistory} variant="outline" size="sm">Vider l'historique</Button>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-1/3">Équation 1</TableHead>
                  <TableHead className="w-1/3">Équation 2</TableHead>
                  <TableHead>Type de Solution</TableHead>
                  <TableHead className="text-right">Point d'Intersection</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {history.map((entry) => (
                  <TableRow key={entry.id}>
                    <TableCell className="font-mono">{entry.equation1}</TableCell>
                    <TableCell className="font-mono">{entry.equation2}</TableCell>
                    <TableCell>{entry.solution_type}</TableCell>
                    <TableCell className="text-right font-mono">
                      {entry.solution
                        ? `(${entry.solution.x.toFixed(2)}, ${entry.solution.y.toFixed(2)})`
                        : 'N/A'}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default LinearSystemSolver;
