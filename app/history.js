import React, { useEffect, useMemo, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Pressable,
  TextInput,
} from "react-native";
import { router } from "expo-router";

import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { radius } from "../src/theme/radius";
import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";
import { getHistory, clearHistory } from "../src/utils/storage";

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

const FilterPill = ({ label, active, onPress }) => (
  <Pressable
    onPress={onPress}
    style={({ pressed }) => [
      styles.pill,
      active && styles.pillActive,
      pressed && { opacity: 0.92 },
    ]}
  >
    <Text style={[styles.pillText, active && styles.pillTextActive]}>
      {label}
    </Text>
  </Pressable>
);

function normalizeType(t) {
  const x = String(t || "").toLowerCase();
  if (x.includes("cumle")) return "cumle";
  if (x.includes("parag")) return "paragraf";
  return x;
}

// ✅ Türkçe karakterleri normalize ederek arama
function normalizeText(s) {
  return String(s || "")
    .toLowerCase()
    .trim()
    .replace(/ğ/g, "g")
    .replace(/ü/g, "u")
    .replace(/ş/g, "s")
    .replace(/ı/g, "i")
    .replace(/ö/g, "o")
    .replace(/ç/g, "c")
    .replace(/\s+/g, " "); // fazla boşlukları teke indir
}

export default function History() {
  const [items, setItems] = useState([]);

  // Kullanıcı yazıyor
  const [draftQuery, setDraftQuery] = useState("");
  // ARA basınca sabitlenecek (ama basmadan da çalışsın)
  const [query, setQuery] = useState("");

  const [typeFilter, setTypeFilter] = useState("all"); // all | cumle | paragraf

  const load = async () => {
    const list = await getHistory();
    // ✅ en yeni üstte olsun
    setItems(Array.isArray(list) ? list : []);
  };

  useEffect(() => {
    load();
  }, []);

  const filtered = useMemo(() => {
    // ✅ ARA'ya basmasa bile arama çalışsın:
    const effectiveQuery = normalizeText(query || draftQuery);

    return (items || []).filter((it) => {
      const t = normalizeType(it?.type);

      // type filtresi
      const okType = typeFilter === "all" ? true : t === typeFilter;

      // arama alanları
      const topic = normalizeText(it?.topic);
      const year = normalizeText(it?.year);
      const typeText = normalizeText(t === "cumle" ? "cumlede" : t === "paragraf" ? "paragraf" : t);

      // ✅ query varsa topic/year/type içinde ara
      const okQuery = effectiveQuery
        ? `${topic} ${year} ${typeText}`.includes(effectiveQuery)
        : true;

      return okType && okQuery;
    });
  }, [items, query, draftQuery, typeFilter]);

  const headerText = useMemo(() => {
    if (!items.length) return "Henüz çözülmüş soru yok.";
    return `Toplam ${items.length} kayıt • Gösterilen ${filtered.length}`;
  }, [items.length, filtered.length]);

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.header}>
        <Text style={styles.title}>Soru Geçmişi</Text>
        <Text style={styles.sub}>{headerText}</Text>

        <View style={{ height: 12 }} />

        {/* Arama + ARA */}
        <View style={styles.searchRow}>
          <TextInput
            value={draftQuery}
            onChangeText={setDraftQuery}
            placeholder="Ara: konu / yıl / tür (ör. ana dusunce, 2024, cumle)"
            placeholderTextColor="#9CA3AF"
            style={styles.search}
            returnKeyType="search"
            onSubmitEditing={() => setQuery(draftQuery)}
          />
          <Pressable
            onPress={() => setQuery(draftQuery)}
            style={({ pressed }) => [styles.searchBtn, pressed && { opacity: 0.92 }]}
          >
            <Text style={styles.searchBtnText}>ARA</Text>
          </Pressable>
        </View>

        <View style={{ height: 12 }} />

        {/* Filtreler */}
        <View style={styles.pillRow}>
          <FilterPill
            label="Tümü"
            active={typeFilter === "all"}
            onPress={() => setTypeFilter("all")}
          />
          <FilterPill
            label="Cümlede"
            active={typeFilter === "cumle"}
            onPress={() => setTypeFilter("cumle")}
          />
          <FilterPill
            label="Paragraf"
            active={typeFilter === "paragraf"}
            onPress={() => setTypeFilter("paragraf")}
          />
        </View>

        <View style={{ height: 12 }} />

        <View style={{ flexDirection: "row", gap: 10 }}>
          <View style={{ flex: 1 }}>
            <TxButton title="YENİLE" variant="outline" onPress={load} />
          </View>
          <View style={{ flex: 1 }}>
            <TxButton
              title="TEMİZLE"
              variant="dark"
              onPress={async () => {
                await clearHistory();
                setDraftQuery("");
                setQuery("");
                setTypeFilter("all");
                await load();
              }}
            />
          </View>
        </View>
      </View>

      <FlatList
        contentContainerStyle={{ padding: spacing.xl, paddingBottom: 40 }}
        data={filtered}
        keyExtractor={(it) => it.id}
        ItemSeparatorComponent={() => <View style={{ height: 12 }} />}
        renderItem={({ item }) => (
          <Pressable
            onPress={() =>
              router.push(
                `/question?id=${encodeURIComponent(item.qid)}&mode=${encodeURIComponent(
                  normalizeType(item.type)
                )}&topic=${encodeURIComponent(item.topic || "")}&year=${encodeURIComponent(
                  item.year || ""
                )}`
              )
            }
            style={({ pressed }) => [pressed && { opacity: 0.92 }]}
          >
            <TxCard>
              <View style={styles.row}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.rowTitle}>{item.topic || "Konu"}</Text>
                  <Text style={styles.rowSub}>
                    {formatTRDate(item.date)} •{" "}
                    {normalizeType(item.type) === "cumle" ? "Cümlede" : "Paragraf"} •{" "}
                    {item.year || "-"}
                  </Text>
                </View>

                <View
                  style={[
                    styles.badge,
                    item.success === 100 ? styles.ok : styles.bad,
                  ]}
                >
                  <Text style={styles.badgeText}>%{item.success}</Text>
                </View>
              </View>
            </TxCard>
          </Pressable>
        )}
        ListEmptyComponent={
          <View style={{ padding: spacing.xl }}>
            <Text style={{ color: colors.textSecondary, fontWeight: "700" }}>
              Filtreye uygun kayıt bulunamadı.
            </Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: spacing.xl, paddingTop: spacing.xl },
  title: { fontSize: 22, fontWeight: "900", color: colors.textPrimary },
  sub: { marginTop: 6, color: colors.textSecondary, fontWeight: "700" },

  searchRow: { flexDirection: "row", gap: 10 },
  search: {
    flex: 1,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.md,
    paddingHorizontal: 12,
    paddingVertical: 12,
    fontWeight: "800",
    color: colors.textPrimary,
    backgroundColor: "#fff",
  },
  searchBtn: {
    paddingHorizontal: 14,
    borderRadius: radius.md,
    backgroundColor: colors.textPrimary,
    justifyContent: "center",
    alignItems: "center",
  },
  searchBtnText: { color: "#fff", fontWeight: "900" },

  pillRow: { flexDirection: "row", gap: 10 },
  pill: {
    flex: 1,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 999,
    paddingVertical: 10,
    alignItems: "center",
    backgroundColor: "#fff",
  },
  pillActive: {
    backgroundColor: "rgba(239,68,68,0.12)",
    borderColor: "rgba(239,68,68,0.35)",
  },
  pillText: { fontWeight: "900", color: colors.textPrimary },
  pillTextActive: { color: colors.primary },

  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
  },
  rowTitle: { fontSize: 16, fontWeight: "900", color: colors.textPrimary },
  rowSub: { marginTop: 6, color: colors.textSecondary, fontWeight: "700" },

  badge: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 999,
    minWidth: 60,
    alignItems: "center",
    justifyContent: "center",
  },
  ok: { backgroundColor: "rgba(22,163,74,0.12)" },
  bad: { backgroundColor: "rgba(239,68,68,0.12)" },
  badgeText: { fontWeight: "900", color: colors.textPrimary },
});
