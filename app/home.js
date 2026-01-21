import React, { useEffect, useMemo, useState } from "react";
import { View, Text, StyleSheet, Pressable, FlatList } from "react-native";
import { router } from "expo-router";

import TxCard from "../src/components/TxCard";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { getHistory } from "../src/utils/storage";

function formatTRDate(iso) {
  try {
    const d = new Date(iso);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}.${month}.${year}`;
  } catch {
    return "-";
  }
}

const ActionCard = ({ title, desc, onPress }) => (
  <Pressable
    onPress={onPress}
    style={({ pressed }) => [pressed && { opacity: 0.92 }]}
  >
    <TxCard style={{ padding: 16 }}>
      <Text style={styles.actionTitle}>{title}</Text>
      <Text style={styles.actionDesc}>{desc}</Text>
      <Text style={styles.actionLink}>Devam →</Text>
    </TxCard>
  </Pressable>
);

export default function Home() {
  const [items, setItems] = useState([]);

  const load = async () => {
    const list = await getHistory();
    setItems(list);
  };

  useEffect(() => {
    const t = setTimeout(load, 50);
    return () => clearTimeout(t);
  }, []);

  const last = useMemo(() => items.slice(0, 5), [items]);

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.header}>
        <Text style={styles.h1}>
          Merhaba, <Text style={{ color: colors.primary }}>Bulut</Text>
        </Text>
        <Text style={styles.p}>
          TahminX ile LGS Türkçe anlam sorularını hızlıca pratik yap.
        </Text>
      </View>

      <View style={styles.body}>
        <View style={{ gap: 12 }}>
          <ActionCard
            title="TahminX AI"
            desc="Konu ve yılı seç, anında sorular gelsin."
            onPress={() => router.push("/ai")}
          />
          <ActionCard
            title="Sana Özel Sorular"
            desc="Kendi seviyene göre hazırlanmış sorular."
            onPress={() => router.push("/special")}
          />
        </View>

        <View style={{ height: 18 }} />

        <View style={styles.sectionRow}>
          <Text style={styles.sectionTitle}>Son Çözülenler</Text>
          <Pressable onPress={() => router.push("/history")}>
            <Text style={styles.sectionLink}>Tümü</Text>
          </Pressable>
        </View>

        <FlatList
          data={last}
          keyExtractor={(it) => it.id}
          ItemSeparatorComponent={() => <View style={{ height: 10 }} />}
          ListEmptyComponent={
            <TxCard style={{ padding: 16 }}>
              <Text style={{ color: colors.textSecondary, fontWeight: "800" }}>
                Henüz çözüm yok. AI ekranından soru çözmeye başla.
              </Text>
            </TxCard>
          }
          renderItem={({ item }) => (
            <Pressable
              onPress={() =>
                router.push(
                  `/question?id=${encodeURIComponent(item.qid)}&mode=${encodeURIComponent(
                    item.type
                  )}&topic=${encodeURIComponent(item.topic || "")}&year=${encodeURIComponent(
                    item.year || ""
                  )}`
                )
              }
              style={({ pressed }) => [pressed && { opacity: 0.92 }]}
            >
              <TxCard style={{ padding: 14 }}>
                <View style={styles.row}>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.rowTitle}>{item.topic}</Text>
                    <Text style={styles.rowSub}>
                      {formatTRDate(item.date)} •{" "}
                      {item.type === "cumle" ? "Cümlede" : "Paragraf"}
                    </Text>
                  </View>
                  <View
                    style={[
                      styles.badge,
                      item.success === 100 ? styles.ok : styles.bad,
                    ]}
                  >
                    <Text style={styles.badgeText}>
                      {item.success === 100 ? "Doğru" : "Yanlış"}
                    </Text>
                  </View>
                </View>
              </TxCard>
            </Pressable>
          )}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: spacing.xl, paddingTop: spacing.xl, gap: 8 },
  h1: { fontSize: 24, fontWeight: "900", color: colors.textPrimary },
  p: { color: colors.textSecondary, fontWeight: "700", lineHeight: 20 },

  body: { padding: spacing.xl, flex: 1 },

  actionTitle: { fontSize: 16, fontWeight: "900", color: colors.textPrimary },
  actionDesc: {
    marginTop: 6,
    color: colors.textSecondary,
    fontWeight: "700",
    lineHeight: 20,
  },
  actionLink: { marginTop: 10, color: colors.primary, fontWeight: "900" },

  sectionRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 10,
  },
  sectionTitle: { fontSize: 16, fontWeight: "900", color: colors.textPrimary },
  sectionLink: { color: colors.primary, fontWeight: "900" },

  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
  },
  rowTitle: { fontSize: 14, fontWeight: "900", color: colors.textPrimary },
  rowSub: { marginTop: 4, color: colors.textSecondary, fontWeight: "700" },

  badge: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 999 },
  ok: { backgroundColor: "rgba(22,163,74,0.12)" },
  bad: { backgroundColor: "rgba(239,68,68,0.12)" },
  badgeText: { fontWeight: "900", color: colors.textPrimary },
});
