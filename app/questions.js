import React, { useMemo } from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import TxCard from "../src/components/TxCard";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { mockQuestions } from "../src/data/questions";

export default function Questions() {
  const params = useLocalSearchParams();
  const mode = Array.isArray(params.mode) ? params.mode[0] : params.mode;
  const topic = Array.isArray(params.topic) ? params.topic[0] : params.topic;
  const year = Array.isArray(params.year) ? params.year[0] : params.year;

  const data = useMemo(() => {
    return mockQuestions.filter((q) => {
      const okType = mode ? q.type === mode : true;
      const okTopic = topic ? q.topic === topic : true;
      const okYear = year ? q.year === year : true;
      return okType && okTopic && okYear;
    });
  }, [mode, topic, year]);

  const modeLabel =
    mode === "cumle"
      ? "Cümlede Anlam"
      : mode === "paragraf"
      ? "Paragrafta Anlam"
      : "Tümü";

  const goQuestion = (id) => {
    router.push(
      `/question?id=${encodeURIComponent(id)}&mode=${encodeURIComponent(
        mode || ""
      )}&topic=${encodeURIComponent(topic || "")}&year=${encodeURIComponent(
        year || ""
      )}`
    );
  };

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.header}>
        <Text style={styles.title}>Sorular</Text>
        <Text style={styles.sub}>
          {modeLabel} • {topic || "Tüm Konular"} • {year || "Tüm Yıllar"}
        </Text>
      </View>

      <FlatList
        contentContainerStyle={{ padding: spacing.xl, paddingBottom: 40 }}
        data={data}
        keyExtractor={(item) => item.id}
        ItemSeparatorComponent={() => <View style={{ height: 12 }} />}
        renderItem={({ item, index }) => (
          <Pressable onPress={() => goQuestion(item.id)}>
            <TxCard>
              <View style={styles.rowBetween}>
                <Text style={styles.qTitle}>Soru {index + 1}</Text>
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>
                    {item.type === "cumle" ? "Cümlede" : "Paragraf"}
                  </Text>
                </View>
              </View>

              <Text style={styles.meta}>
                {item.topic} • {item.year}
              </Text>

              <Text style={styles.qText} numberOfLines={3}>
                {item.question}
              </Text>
            </TxCard>
          </Pressable>
        )}
        ListEmptyComponent={
          <View style={{ padding: spacing.xl }}>
            <Text style={{ color: colors.textSecondary, fontWeight: "700" }}>
              Seçimlerine uygun soru bulunamadı.
            </Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: spacing.xl, paddingTop: spacing.xl, gap: 6 },
  title: { fontSize: 22, fontWeight: "900", color: colors.textPrimary },
  sub: { color: colors.textSecondary, fontWeight: "700" },

  rowBetween: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  qTitle: { fontSize: 16, fontWeight: "900", color: colors.textPrimary },
  meta: { marginTop: 6, color: colors.textSecondary, fontWeight: "700" },
  qText: {
    marginTop: 10,
    color: colors.textPrimary,
    fontWeight: "700",
    lineHeight: 20,
  },

  badge: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
    backgroundColor: "rgba(239,68,68,0.12)",
  },
  badgeText: { color: colors.primary, fontWeight: "900", fontSize: 12 },
});
