// app/profile.js
import React, { useMemo, useState } from "react";
import { View, Text, StyleSheet, Alert } from "react-native";
import { useFocusEffect, router } from "expo-router";

import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";

import { getProfileStats, resetProfileStats } from "../src/utils/profile";
import { logoutUser, getCurrentUser } from "../src/utils/auth";
import { getHistory } from "../src/utils/storage";

// ---- date helpers ----
function toDayKey(dateLike) {
  try {
    const d = new Date(dateLike);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`; // YYYY-MM-DD
  } catch {
    return "";
  }
}

function dayLabelTR(dayKey) {
  // "2025-12-21" -> "21/12"
  const parts = String(dayKey).split("-");
  if (parts.length !== 3) return dayKey;
  return `${parts[2]}/${parts[1]}`;
}

function lastNDays(n) {
  const out = [];
  const now = new Date();
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(now.getDate() - i);
    out.push(toDayKey(d));
  }
  return out;
}

// ---- simple bar chart ----
function MiniBarChart({ data }) {
  // data: [{ key:"YYYY-MM-DD", label:"21/12", value:3 }]
  const maxVal = Math.max(1, ...data.map((x) => x.value || 0));

  return (
    <View style={styles.chartWrap}>
      {data.map((d) => {
        const h = Math.round((80 * (d.value || 0)) / maxVal); // 0..80 px
        return (
          <View key={d.key} style={styles.barCol}>
            <Text style={styles.barTop}>{d.value}</Text>

            <View style={styles.barBase}>
              <View style={[styles.barFill, { height: h }]} />
            </View>

            <Text style={styles.barLabel}>{d.label}</Text>
          </View>
        );
      })}
    </View>
  );
}

export default function Profile() {
  const [stats, setStats] = useState({
    totalSolved: 0,
    correct: 0,
    wrong: 0,
  });

  const [user, setUser] = useState(null);
  const [history, setHistory] = useState([]);

  // ✅ Sayfa her açıldığında verileri yenile
  useFocusEffect(
    React.useCallback(() => {
      let mounted = true;

      const run = async () => {
        const [s, u, h] = await Promise.all([
          getProfileStats(),
          getCurrentUser(),
          getHistory(), // ✅ legacy key'lerden de çekip migrate eder (storage.js güncelse)
        ]);

        if (!mounted) return;
        setStats(s);
        setUser(u);
        setHistory(Array.isArray(h) ? h : []);
      };

      run();
      return () => {
        mounted = false;
      };
    }, [])
  );

  const accuracy =
    stats.totalSolved > 0
      ? Math.round((stats.correct / stats.totalSolved) * 100)
      : 0;

  // ✅ Son 7 gün grafiği
  const chartData = useMemo(() => {
    const days = lastNDays(7);

    const counts = {};
    for (const it of history) {
      const key = toDayKey(it?.date);
      if (!key) continue;
      counts[key] = (counts[key] || 0) + 1;
    }

    return days.map((k) => ({
      key: k,
      label: dayLabelTR(k),
      value: counts[k] || 0,
    }));
  }, [history]);

  const totalLast7 = useMemo(
    () => chartData.reduce((a, b) => a + (b.value || 0), 0),
    [chartData]
  );

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.container}>
        {/* Kullanıcı Kartı */}
        <TxCard>
          <Text style={styles.name}>{user?.name || "Kullanıcı"}</Text>
          <Text style={styles.email}>{user?.email || ""}</Text>
        </TxCard>

        {/* İstatistikler */}
        <TxCard>
          <Text style={styles.sectionTitle}>İstatistikler</Text>

          <View style={styles.row}>
            <Text style={styles.label}>Toplam Çözülen</Text>
            <Text style={styles.value}>{stats.totalSolved}</Text>
          </View>

          <View style={styles.row}>
            <Text style={styles.label}>Doğru</Text>
            <Text style={[styles.value, { color: "#16a34a" }]}>{stats.correct}</Text>
          </View>

          <View style={styles.row}>
            <Text style={styles.label}>Yanlış</Text>
            <Text style={[styles.value, { color: "#dc2626" }]}>{stats.wrong}</Text>
          </View>

          <View style={styles.row}>
            <Text style={styles.label}>Başarı Oranı</Text>
            <Text style={styles.value}>%{accuracy}</Text>
          </View>
        </TxCard>

        {/* Grafik */}
        <TxCard>
          <View style={styles.chartHeader}>
            <Text style={styles.sectionTitle}>Son 7 Gün</Text>
            <Text style={styles.chartSub}>Toplam: {totalLast7}</Text>
          </View>

          {totalLast7 === 0 ? (
            <Text style={styles.noData}>
              Son 7 günde çözülmüş soru yok. 1-2 soru çöz, grafik dolacak.
            </Text>
          ) : null}

          <MiniBarChart data={chartData} />

          <Text style={styles.hint}>
            Not: Grafik, “Soru Geçmişi” kayıtlarına göre güncellenir.
          </Text>
        </TxCard>

        {/* Aksiyonlar */}
        <TxCard>
          <TxButton
            title="İSTATİSTİKLERİ SIFIRLA"
            variant="outline"
            onPress={() => {
              Alert.alert("Emin misin?", "Tüm istatistikler sıfırlanacak.", [
                { text: "Vazgeç", style: "cancel" },
                {
                  text: "Sıfırla",
                  style: "destructive",
                  onPress: async () => {
                    await resetProfileStats();
                    const fresh = await getProfileStats();
                    setStats(fresh);
                  },
                },
              ]);
            }}
          />

          <View style={{ height: 10 }} />

          <TxButton
            title="ÇIKIŞ YAP"
            variant="dark"
            onPress={async () => {
              await logoutUser();
              router.replace("/login");
            }}
          />
        </TxCard>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.xl, gap: 12 },

  name: { fontSize: 20, fontWeight: "900", color: colors.textPrimary },
  email: { marginTop: 4, fontWeight: "700", color: colors.textSecondary },

  sectionTitle: {
    fontSize: 14,
    fontWeight: "900",
    color: colors.textSecondary,
    marginBottom: 12,
  },

  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 6,
  },
  label: { fontWeight: "800", color: colors.textPrimary },
  value: { fontWeight: "900", color: colors.textPrimary },

  chartHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "baseline",
  },
  chartSub: { color: colors.textSecondary, fontWeight: "800" },

  noData: {
    color: colors.textSecondary,
    fontWeight: "800",
    marginBottom: 8,
  },

  chartWrap: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-end",
    paddingTop: 6,
    paddingBottom: 6,
  },
  barCol: { width: 36, alignItems: "center", gap: 6 },
  barTop: { fontWeight: "900", color: colors.textSecondary, fontSize: 12 },

  barBase: {
    width: 16,
    height: 80,
    borderRadius: 10,
    backgroundColor: "rgba(17,24,39,0.08)",
    justifyContent: "flex-end",
    overflow: "hidden",
  },
  barFill: {
    width: "100%",
    borderRadius: 10,
    backgroundColor: colors.primary,
  },
  barLabel: { fontWeight: "900", color: colors.textSecondary, fontSize: 11 },

  hint: {
    marginTop: 10,
    color: colors.textSecondary,
    fontWeight: "700",
    lineHeight: 18,
    fontSize: 12,
  },
});
