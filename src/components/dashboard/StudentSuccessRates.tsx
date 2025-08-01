import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Progress } from '@/components/ui/progress';

interface StudentSuccessRate {
  studentId: string;
  studentName: string;
  modules: {
    moduleId: string;
    moduleName: string;
    successRate: number;
    completedQuizzes: number;
    totalQuizzes: number;
  }[];
  overallSuccess: number;
}

interface StudentSuccessRatesProps {
  data: StudentSuccessRate[];
  className?: string;
}

export function StudentSuccessRates({ data, className }: StudentSuccessRatesProps) {
  if (data.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Taux de Réussite par Étudiant</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">Aucune donnée disponible pour le moment</p>
        </CardContent>
      </Card>
    );
  }

  // Get all unique module names for table headers
  const moduleNames = Array.from(
    new Set(
      data.flatMap(student => 
        student.modules.map(module => module.moduleName)
      )
    )
  );

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Taux de Réussite par Étudiant</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Étudiant</TableHead>
                {moduleNames.map(moduleName => (
                  <TableHead key={moduleName} className="text-center">
                    <div className="text-xs text-muted-foreground">{moduleName}</div>
                  </TableHead>
                ))}
                <TableHead className="text-right">Moyenne</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.map((student) => (
                <TableRow key={student.studentId}>
                  <TableCell className="font-medium">{student.studentName}</TableCell>
                  {moduleNames.map(moduleName => {
                    const moduleData = student.modules.find(m => m.moduleName === moduleName);
                    return (
                      <TableCell key={`${student.studentId}-${moduleName}`} className="p-2">
                        {moduleData ? (
                          <div className="flex flex-col items-center">
                            <Progress 
                              value={moduleData.successRate} 
                              className="h-2 w-16 mb-1" 
                            />
                            <span className="text-xs text-muted-foreground">
                              {moduleData.completedQuizzes}/{moduleData.totalQuizzes}
                            </span>
                          </div>
                        ) : (
                          <div className="h-8 flex items-center justify-center">
                            <span className="text-xs text-muted-foreground">-</span>
                          </div>
                        )}
                      </TableCell>
                    );
                  })}
                  <TableCell className="text-right font-medium">
                    {Math.round(student.overallSuccess)}%
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}

// Données factices pour la prévisualisation
export const mockStudentSuccessData: StudentSuccessRate[] = [
  {
    studentId: '1',
    studentName: 'Jean Dupont',
    overallSuccess: 78,
    modules: [
      {
        moduleId: 'm1',
        moduleName: 'Algèbre',
        successRate: 85,
        completedQuizzes: 4,
        totalQuizzes: 5
      },
      {
        moduleId: 'm2',
        moduleName: 'Géométrie',
        successRate: 70,
        completedQuizzes: 2,
        totalQuizzes: 3
      },
      {
        moduleId: 'm3',
        moduleName: 'Analyse',
        successRate: 80,
        completedQuizzes: 3,
        totalQuizzes: 4
      }
    ]
  },
  {
    studentId: '2',
    studentName: 'Marie Martin',
    overallSuccess: 92,
    modules: [
      {
        moduleId: 'm1',
        moduleName: 'Algèbre',
        successRate: 95,
        completedQuizzes: 5,
        totalQuizzes: 5
      },
      {
        moduleId: 'm2',
        moduleName: 'Géométrie',
        successRate: 90,
        completedQuizzes: 3,
        totalQuizzes: 3
      },
      {
        moduleId: 'm3',
        moduleName: 'Analyse',
        successRate: 90,
        completedQuizzes: 4,
        totalQuizzes: 4
      }
    ]
  }
];
