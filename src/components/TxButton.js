import React from "react";
import { Pressable, Text, StyleSheet, ActivityIndicator } from "react-native";
import { colors } from "../theme/colors";
import { radius } from "../theme/radius";
import { spacing } from "../theme/spacing";

export default function TxButton({
  title,
  onPress,
  variant = "primary", // primary | outline | dark
  loading = false,
  style,
}) {
  const isOutline = variant === "outline";
  const isDark = variant === "dark";

  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [
        styles.base,
        isOutline && styles.outline,
        isDark && styles.dark,
        pressed && { opacity: 0.9 },
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator color="#fff" />
      ) : (
        <Text
          style={[
            styles.text,
            isOutline && { color: colors.textPrimary },
            isDark && { color: "#fff" },
          ]}
        >
          {title}
        </Text>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    backgroundColor: colors.primary,
    paddingVertical: 14,
    borderRadius: radius.md,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 3,
  },
  outline: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: colors.border,
  },
  dark: {
    backgroundColor: colors.textPrimary,
  },
  text: {
    color: "#fff",
    fontSize: 15,
    fontWeight: "700",
  },
});
