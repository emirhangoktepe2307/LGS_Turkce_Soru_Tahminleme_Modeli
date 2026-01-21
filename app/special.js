import React from "react";
import { View, Text, StyleSheet, Pressable, FlatList } from "react-native";
import { router } from "expo-router";

import TxCard from "../src/components/TxCard";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { specialSets } from "../src/data/specialSets";

const LevelPill = ({ level }) => {
  const isHard = level === "Zor";
  const isMid = level === "Orta";
  return (
    <View
      style={[
        styles.pill,
        isHard && styles.pillHard,
        isMid && styles.pillMid,
      ]}
    >
      <Text style={styles.pillText}>{level}</Text>
    </View>
  );
};

const SetCard = ({ item }) => (
  <Pressable
    onPress={() =>
      router.push(
        `/questions?mode=${encodeURIComponent(item.mode)}&topic=${encodeURIComponent(
          item.topic
        )}&year=${encodeURIComponent(item.year)}`
      )
    }
    style={({ pressed }) => [pressed && { opacity: 0.92 }]}
  >
    <TxCard style={{ padding: 16 }}>
      <View style={styles.rowBetween}>
        <Text style={styles.cardTitle}>{item.title}</Text>
        <LevelPill level={item.level} />
      </View>

      <Text style={styles.cardDesc}>{item.desc}</Text>

      <View style={{ height: 10 }} />

      <Text style={styles.link}>Başla →</Text>
    </TxCard>
  </Pressable>
);

export default function Special() {
  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.header}>
        <Text style={styles.h1}>Sana Özel Sorular</Text>
        <Text style={styles.p}>
          Çözüm geçmişine göre hazırlanmış örnek setler.
        </Text>
      </View>

      <View style={{ paddingHorizontal: spacing.xl, marginTop: 12 }}>
        <TxCard style={{ padding: 16 }}>
          <Text style={styles.sectionTitle}>Önerilen</Text>
          <Text style={styles.sectionSub}>
            Bugün 10-15 soru çöz, ritmini yakala.
          </Text>

          <View style={{ height: 12 }} />

          <View style={styles.suggestRow}>
            <Pressable
              style={({ pressed }) => [styles.suggest, pressed && { opacity: 0.9 }]}
              onPress={() => router.push(`/questions?mode=cumle&topic=&year=2025`)}
            >
              <Text style={styles.suggestTitle}>Kolay</Text>
              <Text style={styles.suggestSub}>Isınma</Text>
            </Pressable>

            <Pressable
              style={({ pressed }) => [styles.suggest, pressed && { opacity: 0.9 }]}
              onPress={() => router.push(`/questions?mode=paragraf&topic=&year=2025`)}
            >
              <Text style={styles.suggestTitle}>Orta</Text>
              <Text style={styles.suggestSub}>Odak</Text>
            </Pressable>

            <Pressable
              style={({ pressed }) => [styles.suggest, pressed && { opacity: 0.9 }]}
              onPress={() => router.push(`/questions?mode=paragraf&topic=&year=2024`)}
            >
              <Text style={styles.suggestTitle}>Zor</Text>
              <Text style={styles.suggestSub}>Meydan Oku</Text>
            </Pressable>
          </View>
        </TxCard>
      </View>

      <FlatList
        contentContainerStyle={{ padding: spacing.xl, paddingBottom: 40 }}
        data={specialSets}
        keyExtractor={(it) => it.id}
        ItemSeparatorComponent={() => <View style={{ height: 12 }} />}
        renderItem={({ item }) => <SetCard item={item} />}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: spacing.xl, paddingTop: spacing.xl, gap: 8 },
  h1: { fontSize: 22, fontWeight: "900", color: colors.textPrimary },
  p: { color: colors.textSecondary, fontWeight: "700", lineHeight: 20 },

  sectionTitle: { fontSize: 14, fontWeight: "900", color: colors.textPrimary },
  sectionSub: { marginTop: 6, color: colors.textSecondary, fontWeight: "700" },

  suggestRow: { flexDirection: "row", gap: 10 },
  suggest: {
    flex: 1,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: "center",
    backgroundColor: "#fff",
  },
  suggestTitle: { fontWeight: "900", color: colors.textPrimary, fontSize: 14 },
  suggestSub: { marginTop: 4, color: colors.textSecondary, fontWeight: "700" },

  rowBetween: { flexDirection: "row", alignItems: "center", justifyContent: "space-between" },
  cardTitle: { fontSize: 16, fontWeight: "900", color: colors.textPrimary },
  cardDesc: { marginTop: 8, color: colors.textSecondary, fontWeight: "700", lineHeight: 20 },
  link: { color: colors.primary, fontWeight: "900" },

  pill: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
    backgroundColor: "rgba(22,163,74,0.12)",
  },
  pillMid: { backgroundColor: "rgba(59,130,246,0.12)" },
  pillHard: { backgroundColor: "rgba(239,68,68,0.12)" },
  pillText: { fontWeight: "900", color: colors.textPrimary, fontSize: 12 },
});
