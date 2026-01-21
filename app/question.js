// app/question.js
import React, { useMemo, useState, useEffect } from "react";
import { View, Text, StyleSheet, Pressable, ScrollView, Alert } from "react-native";
import { useLocalSearchParams, router } from "expo-router";

import { mockQuestions } from "../src/data/questions";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { radius } from "../src/theme/radius";
import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";

import { updateProfileStats } from "../src/utils/profile";
import { addHistoryEntry } from "../src/utils/storage";

function ChoiceCard({ label, text, selected, disabled, onPress }) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.choice,
        selected && styles.choiceSelected,
        pressed && !disabled && { opacity: 0.9 },
        disabled && { opacity: 0.75 },
      ]}
    >
      <View style={[styles.choiceBadge, selected && styles.choiceBadgeSelected]}>
        <Text style={[styles.choiceBadgeText, selected && { color: "#fff" }]}>{label}</Text>
      </View>
      <Text style={styles.choiceText}>{text}</Text>
    </Pressable>
  );
}

export default function Question() {
  const params = useLocalSearchParams();

  const idRaw = params?.id;
  const id = String(Array.isArray(idRaw) ? idRaw[0] : idRaw || "");

  const modeRaw = params?.mode;
  const topicRaw = params?.topic;
  const yearRaw = params?.year;

  const mode = String(Array.isArray(modeRaw) ? modeRaw[0] : modeRaw || "");
  const topic = decodeURIComponent(String(Array.isArray(topicRaw) ? topicRaw[0] : topicRaw || ""));
  const year = String(Array.isArray(yearRaw) ? yearRaw[0] : yearRaw || "");

  const q = useMemo(() => mockQuestions.find((x) => String(x.id) === id), [id]);

  const [selectedIndex, setSelectedIndex] = useState(null);
  const [checked, setChecked] = useState(false);

  // ✅ Soru değişince seçimleri sıfırla
  useEffect(() => {
    setSelectedIndex(null);
    setChecked(false);
  }, [id]);

  // "Sonraki soru" için aynı filtredeki listeyi hazırla
  const filteredList = useMemo(() => {
    return mockQuestions.filter((x) => {
      const okMode = mode ? x.type === mode : true;
      const okTopic = topic ? String(x.topic) === String(topic) : true;
      const okYear = year ? String(x.year) === String(year) : true;
      return okMode && okTopic && okYear;
    });
  }, [mode, topic, year]);

  const goNext = () => {
    const idx = filteredList.findIndex((x) => String(x.id) === String(id));
    if (idx === -1) {
      router.push("/questions");
      return;
    }
    const next = filteredList[idx + 1];
    if (!next) {
      Alert.alert("Bitti", "Bu filtrede başka soru yok.", [
        { text: "Soru listesine dön", onPress: () => router.push("/questions") },
      ]);
      return;
    }

    router.push(
      `/question?id=${encodeURIComponent(next.id)}&mode=${encodeURIComponent(
        mode
      )}&topic=${encodeURIComponent(topic || "")}&year=${encodeURIComponent(year || "")}`
    );
  };

  if (!q) {
    return (
      <View style={[styles.center, { backgroundColor: colors.background }]}>
        <Text style={{ color: colors.textSecondary, fontWeight: "800" }}>Soru bulunamadı.</Text>
        <View style={{ height: 12 }} />
        <TxButton title="Geri Dön" onPress={() => router.back()} />
      </View>
    );
  }

  const letters = ["A", "B", "C", "D"];
  const isCorrect = checked && selectedIndex !== null && selectedIndex === q.answerIndex;

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: colors.background }}
      contentContainerStyle={styles.container}
    >
      {/* Üst bilgi */}
      <View style={styles.topRow}>
        <Text style={styles.topTitle}>
          {q.type === "cumle" ? "Cümlede Anlam" : "Paragrafta Anlam"}
        </Text>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>
            {q.topic} • {q.year}
          </Text>
        </View>
      </View>

      {/* Paragraf varsa */}
      {q.passage ? (
        <TxCard style={{ padding: 16 }}>
          <Text style={styles.sectionTitle}>Paragraf</Text>
          <Text style={styles.passage}>{q.passage}</Text>
        </TxCard>
      ) : null}

      {/* Soru */}
      <TxCard style={{ padding: 16 }}>
        <Text style={styles.sectionTitle}>Soru</Text>
        <Text style={styles.question}>{q.question}</Text>
      </TxCard>

      {/* Şıklar */}
      <View style={{ gap: 10 }}>
        {q.choices.map((c, idx) => (
          <ChoiceCard
            key={`${q.id}-${idx}`}
            label={letters[idx]}
            text={c}
            selected={selectedIndex === idx}
            disabled={checked}
            onPress={() => setSelectedIndex(idx)}
          />
        ))}
      </View>

      {/* Aksiyon */}
      {!checked ? (
        <TxButton
          title="CEVABI KONTROL ET"
          onPress={async () => {
            if (selectedIndex === null) {
              Alert.alert("Uyarı", "Lütfen bir seçenek işaretle.");
              return;
            }

            const correct = selectedIndex === q.answerIndex;

            setChecked(true);

            // ✅ Profil istatistiğini güncelle
            try {
              await updateProfileStats(correct);
            } catch {}

            // ✅ History kaydı at (soru geçmişi için)
            try {
              await addHistoryEntry({
                qid: q.id,
                type: q.type,
                topic: q.topic,
                year: q.year,
                success: correct ? 100 : 0,
                date: new Date().toISOString(),
              });
            } catch {}
          }}
        />
      ) : (
        <TxCard style={[styles.resultCard, isCorrect ? styles.ok : styles.bad]}>
          <Text style={styles.resultTitle}>{isCorrect ? "Doğru ✅" : "Yanlış ❌"}</Text>

          {!isCorrect ? (
            <Text style={styles.resultText}>
              Doğru cevap: <Text style={{ fontWeight: "900" }}>{letters[q.answerIndex]}</Text>
            </Text>
          ) : (
            <Text style={styles.resultText}>Tebrikler, doğru cevapladın!</Text>
          )}

          <View style={{ height: 12 }} />

          <TxButton title="SONRAKİ SORU" onPress={goNext} />

          <View style={{ height: 10 }} />

          <TxButton
            title="SORU LİSTESİNE DÖN"
            variant="outline"
            onPress={() => router.push("/questions")}
          />
        </TxCard>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.xl, paddingBottom: 50, gap: 12 },
  center: { flex: 1, alignItems: "center", justifyContent: "center", padding: spacing.xl },

  topRow: { gap: 10, marginBottom: 2 },
  topTitle: { fontSize: 22, fontWeight: "900", color: colors.textPrimary },
  badge: {
    alignSelf: "flex-start",
    backgroundColor: "rgba(17,24,39,0.06)",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
  },
  badgeText: { color: colors.textSecondary, fontWeight: "800", fontSize: 12 },

  sectionTitle: { fontSize: 13, fontWeight: "900", color: colors.textSecondary, marginBottom: 8 },
  passage: { color: colors.textPrimary, fontWeight: "700", lineHeight: 20 },
  question: { color: colors.textPrimary, fontWeight: "800", lineHeight: 21 },

  choice: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.lg,
    padding: 14,
    backgroundColor: "#fff",
    flexDirection: "row",
    gap: 12,
    alignItems: "flex-start",
  },
  choiceSelected: {
    borderColor: colors.primary,
    backgroundColor: "rgba(239,68,68,0.06)",
  },
  choiceBadge: {
    width: 28,
    height: 28,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#fff",
  },
  choiceBadgeSelected: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  choiceBadgeText: { fontWeight: "900", color: colors.textPrimary },
  choiceText: { flex: 1, color: colors.textPrimary, fontWeight: "700", lineHeight: 20 },

  resultCard: { padding: 16 },
  ok: { borderWidth: 1, borderColor: "rgba(22,163,74,0.35)" },
  bad: { borderWidth: 1, borderColor: "rgba(239,68,68,0.35)" },
  resultTitle: { fontSize: 18, fontWeight: "900", color: colors.textPrimary },
  resultText: { marginTop: 6, color: colors.textSecondary, fontWeight: "800" },
});
