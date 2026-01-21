// app/ai.js
import React, { useMemo, useState, useEffect } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { router } from "expo-router";

import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";

import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";
import TxSegment from "../src/components/TxSegment";
import TxSelect from "../src/components/TxSelect";
import TxBottomSheet from "../src/components/TxBottomSheet";

import { topicsCumle, topicsParagraf } from "../src/data/topics";
import { years } from "../src/data/stats";

export default function Ai() {
  const [mode, setMode] = useState("cumle");

  const topics = useMemo(
    () => (mode === "cumle" ? topicsCumle : topicsParagraf),
    [mode]
  );

  const [topic, setTopic] = useState(topicsCumle[0]);
  const [year, setYear] = useState(years[0]);

  const [topicOpen, setTopicOpen] = useState(false);
  const [yearOpen, setYearOpen] = useState(false);

  useEffect(() => {
    const list = mode === "cumle" ? topicsCumle : topicsParagraf;
    setTopic(list[0]);
  }, [mode]);

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: colors.background }}
      contentContainerStyle={styles.container}
    >
      <Text style={styles.h1}>
        Soruları Daha <Text style={{ color: colors.primary }}>Akıllı</Text> Üret,
        Daha <Text style={{ color: colors.primary }}>Kolay</Text> Öğren!
      </Text>

      <Text style={styles.p}>
        LGS Türkçe Cümlede Anlam ve Paragrafta Anlam sorularını yapay zekâ ile
        anında oluştur.
      </Text>

      <View style={{ height: 10 }} />

      <TxCard>
        <TxSegment
          value={mode}
          onChange={setMode}
          items={[
            { label: "CÜMLEDE ANLAM", value: "cumle" },
            { label: "PARAGRAFTA ANLAM", value: "paragraf" },
          ]}
        />

        <View style={{ height: 16 }} />

        <View style={styles.row}>
          <TxSelect
            label="KONU"
            value={topic}
            onPress={() => setTopicOpen(true)}
          />
          <View style={{ width: 12 }} />
          <TxSelect
            label="YIL"
            value={year}
            onPress={() => setYearOpen(true)}
          />
        </View>

        <View style={{ height: 18 }} />

        <TxButton
          title="SORULARI GÖR"
          onPress={() =>
            router.push({
              pathname: "/questions",
              params: { mode, topic, year },
            })
          }
        />
      </TxCard>

      <TxBottomSheet
        visible={topicOpen}
        title="Konu Seç"
        items={topics}
        onClose={() => setTopicOpen(false)}
        onSelect={(val) => {
          setTopic(val);
          setTopicOpen(false);
        }}
      />

      <TxBottomSheet
        visible={yearOpen}
        title="Yıl Seç"
        items={years}
        onClose={() => setYearOpen(false)}
        onSelect={(val) => {
          setYear(val);
          setYearOpen(false);
        }}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.xl, paddingBottom: 40, gap: 10 },
  h1: {
    fontSize: 28,
    fontWeight: "900",
    color: colors.textPrimary,
    lineHeight: 34,
  },
  p: { color: colors.textSecondary, fontSize: 14.5, lineHeight: 20 },
  row: { flexDirection: "row" },
});
