import React from "react";
import { Pressable, Text, StyleSheet } from "react-native";
import { router } from "expo-router";
import { colors } from "../theme/colors";

export default function TxHeaderBack() {
  return (
    <Pressable
      onPress={() => {
        try {
          router.back();
        } catch {
          router.replace("/home");
        }
      }}
      style={({ pressed }) => [styles.btn, pressed && { opacity: 0.85 }]}
      hitSlop={12}
    >
      <Text style={styles.arrow}>‹</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  btn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    marginLeft: 10,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(239,68,68,0.10)",
  },
  arrow: {
    fontSize: 22,
    fontWeight: "900",
    color: colors.primary,
    marginTop: -2,
  },
});
