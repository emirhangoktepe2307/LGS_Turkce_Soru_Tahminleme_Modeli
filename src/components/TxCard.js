import React from "react";
import { View, StyleSheet } from "react-native";
import { colors } from "../theme/colors";
import { radius } from "../theme/radius";

export default function TxCard({ children, style }) {
  return <View style={[styles.card, style]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    padding: 16,
    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 18,
    elevation: 2,
  },
});
