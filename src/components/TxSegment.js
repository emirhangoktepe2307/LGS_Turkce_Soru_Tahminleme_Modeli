import React from "react";
import { View, Pressable, Text, StyleSheet } from "react-native";
import { colors } from "../theme/colors";

export default function TxSegment({ value, onChange, items }) {
  return (
    <View style={styles.wrap}>
      {items.map((it) => {
        const active = it.value === value;
        return (
          <Pressable key={it.value} onPress={() => onChange(it.value)} style={styles.item}>
            <Text style={[styles.text, active && styles.textActive]}>{it.label}</Text>
            {active && <View style={styles.underline} />}
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flexDirection: "row", gap: 18, alignItems: "flex-end" },
  item: { paddingVertical: 6 },
  text: { fontSize: 14, fontWeight: "900", color: "#9CA3AF" },
  textActive: { color: colors.textPrimary },
  underline: { height: 3, backgroundColor: colors.primary, borderRadius: 10, marginTop: 6 },
});
