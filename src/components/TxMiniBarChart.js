import React, { useMemo } from "react";
import { View } from "react-native";
import Svg, { Rect } from "react-native-svg";
import { colors } from "../theme/colors";

export default function TxMiniBarChart({
  data = [], // [{ label:"Pzt", value:3 }]
  height = 90,
  barWidth = 18,
  gap = 10,
  radius = 8,
}) {
  const { width, max } = useMemo(() => {
    const w = data.length * barWidth + Math.max(0, data.length - 1) * gap;
    const m = Math.max(1, ...data.map((d) => Number(d.value) || 0));
    return { width: w, max: m };
  }, [data, barWidth, gap]);

  return (
    <View style={{ overflow: "hidden" }}>
      <Svg width={width} height={height}>
        {data.map((d, i) => {
          const v = Number(d.value) || 0;
          const h = Math.max(4, Math.round((v / max) * (height - 10)));
          const x = i * (barWidth + gap);
          const y = height - h;

          return (
            <Rect
              key={d.label + i}
              x={x}
              y={y}
              width={barWidth}
              height={h}
              rx={radius}
              ry={radius}
              fill={colors.primary}
              opacity={0.85}
            />
          );
        })}
      </Svg>
    </View>
  );
}
