import React from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { router } from "expo-router";

import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { radius } from "../src/theme/radius";

export default function ModalScreen() {
  return (
    <View style={styles.wrap}>
      <TxCard style={styles.card}>
        <Text style={styles.title}>Modal</Text>
        <Text style={styles.sub}>
          Bu ekran bir modal örneğidir. İstersen burada “Hakkında / Yardım /
          Ayarlar” gibi içerikler gösterebilirsin.
        </Text>

        <View style={{ height: 12 }} />

        <TxButton title="Kapat" onPress={() => router.back()} />

        <Pressable onPress={() => router.back()} style={styles.linkWrap}>
          <Text style={styles.link}>Geri dön</Text>
        </Pressable>
      </TxCard>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.xl,
    justifyContent: "center",
  },
  card: {
    padding: 16,
    borderRadius: radius.lg,
  },
  title: {
    fontSize: 20,
    fontWeight: "900",
    color: colors.textPrimary,
  },
  sub: {
    marginTop: 8,
    color: colors.textSecondary,
    fontWeight: "700",
    lineHeight: 20,
  },
  linkWrap: { marginTop: 10, alignItems: "center", padding: 8 },
  link: { color: colors.primary, fontWeight: "900" },
});
