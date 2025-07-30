import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface IterationData {
  iteration: number;
  jacobi: number;
  gaussSeidel: number;
}

interface Props {
  jacobiErrors: number[];
  gaussSeidelErrors: number[];
}

const SystemesLineairesGraph: React.FC<Props> = ({ jacobiErrors, gaussSeidelErrors }) => {
  // Prépare les données pour le graphique (même nombre d'itérations, sinon tronque)
  const n = Math.max(jacobiErrors.length, gaussSeidelErrors.length);
  const data: IterationData[] = Array.from({ length: n }, (_, i) => ({
    iteration: i + 1,
    jacobi: jacobiErrors[i] ?? null,
    gaussSeidel: gaussSeidelErrors[i] ?? null,
  }));

  return (
    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 40, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="iteration" label={{ value: "Itérations", position: "insideBottomRight", offset: 0 }} />
          <YAxis label={{ value: "Erreur relative", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="jacobi" stroke="#e74c3c" dot={false} name="Jacobi" />
          <Line type="monotone" dataKey="gaussSeidel" stroke="#2980b9" dot={false} name="Gauss-Seidel" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SystemesLineairesGraph;
