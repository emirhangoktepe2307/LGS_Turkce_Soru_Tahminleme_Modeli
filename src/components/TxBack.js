import React from "react";
import { Pressable, Text, StyleSheet, View } from "react-native";
import { router } from "expo-router";
import { colors } from "../theme/colors";

export default function TxBack({ fallback = "/home" }) {
  return (
    <Pressable
      onPress={() => {
        try {
          router.back();
        } catch (e) {
          router.push(fallback);
        }
      }}
      style={({ pressed }) => [styles.btn, pressed && { opacity: 0.9 }]}
    >
      <View style={styles.dot}>
        <Text style={styles.arrow}>←</Text>
      </View>
      <Text style={styles.text}>Geri</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  btn: { flexDirection: "row", alignItems: "center", gap: 8, paddingVertical: 10 },
  dot: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: "rgba(239,68,68,0.12)",
    alignItems: "center",
    justifyContent: "center",
  },
  arrow: { fontWeight: "900", color: colors.primary, fontSize: 14 },
  text: { fontWeight: "900", color: colors.textPrimary },
});
