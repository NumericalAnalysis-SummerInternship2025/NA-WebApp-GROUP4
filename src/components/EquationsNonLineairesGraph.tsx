import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface DataPoint {
  iteration: number;
  dichotomie?: number;
  newton?: number;
  pointFixe?: number;
}

interface Props {
  dichotomie?: number[]; // Largeur de l'intervalle
  newton?: number[];     // Erreur |x_{k+1} - x_k|
  pointFixe?: number[];  // Distance à la solution
}

const EquationsNonLineairesGraph: React.FC<Props> = ({ dichotomie, newton, pointFixe }) => {
  const n = Math.max(
    dichotomie?.length || 0,
    newton?.length || 0,
    pointFixe?.length || 0
  );
  const data: DataPoint[] = Array.from({ length: n }, (_, i) => ({
    iteration: i + 1,
    dichotomie: dichotomie?.[i] ?? null,
    newton: newton?.[i] ?? null,
    pointFixe: pointFixe?.[i] ?? null,
  }));

  return (
    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 40, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="iteration" label={{ value: "Itérations", position: "insideBottomRight", offset: 0 }} />
          <YAxis label={{ value: "Erreur / Largeur", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Legend />
          {dichotomie && <Line type="monotone" dataKey="dichotomie" stroke="#16a085" dot={false} name="Dichotomie" />}
          {newton && <Line type="monotone" dataKey="newton" stroke="#e67e22" dot={false} name="Newton" />}
          {pointFixe && <Line type="monotone" dataKey="pointFixe" stroke="#8e44ad" dot={false} name="Point Fixe" />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EquationsNonLineairesGraph;
