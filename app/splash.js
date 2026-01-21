import React, { useEffect } from "react";
import { View, Text, StyleSheet } from "react-native";
import { router } from "expo-router";
import { colors } from "../src/theme/colors";
import { isLoggedIn } from "../src/utils/auth";

export default function Splash() {
  useEffect(() => {
    let mounted = true;

    const run = async () => {
      const ok = await isLoggedIn();
      setTimeout(() => {
        if (!mounted) return;
        router.replace(ok ? "/home" : "/login");
      }, 650);
    };

    run();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <View style={styles.wrap}>
      <Text style={styles.tx}>TX</Text>
      <Text style={styles.name}>TahminX</Text>
      <Text style={styles.sub}>LGS Türkçe • Yapay Zeka</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    flex: 1,
    backgroundColor: colors.background,
    alignItems: "center",
    justifyContent: "center",
  },
  tx: { fontSize: 42, fontWeight: "900", color: colors.textPrimary },
  name: { marginTop: 6, fontSize: 22, fontWeight: "900", color: colors.primary },
  sub: { marginTop: 8, fontWeight: "700", color: colors.textSecondary },
});
