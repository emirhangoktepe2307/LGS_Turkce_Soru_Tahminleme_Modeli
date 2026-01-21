import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { colors } from "../theme/colors";
import { radius } from "../theme/radius";

export default function TxSelect({ label, value, onPress }) {
  return (
    <View style={{ flex: 1 }}>
      <Text style={styles.label}>{label}</Text>
      <Pressable onPress={onPress} style={({ pressed }) => [styles.select, pressed && { opacity: 0.9 }]}>
        <Text style={styles.value}>{value}</Text>
        <Text style={styles.chev}>▾</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  label: { color: "#9CA3AF", fontWeight: "900", fontSize: 12, marginBottom: 8 },
  select: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.md,
    paddingHorizontal: 12,
    paddingVertical: 12,
    backgroundColor: "#fff",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  value: { color: colors.textPrimary, fontWeight: "800" },
  chev: { color: "#9CA3AF", fontSize: 16, fontWeight: "900" },
});
