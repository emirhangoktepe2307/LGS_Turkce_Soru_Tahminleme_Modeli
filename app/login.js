import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TextInput, Pressable, Alert } from "react-native";
import { router, useLocalSearchParams } from "expo-router";

import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { radius } from "../src/theme/radius";
import { loginUser } from "../src/utils/auth";

export default function Login() {
  const params = useLocalSearchParams();
  const emailParamRaw = params?.email;
  const emailParam = decodeURIComponent(String(Array.isArray(emailParamRaw) ? emailParamRaw[0] : emailParamRaw || ""));

  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");

  useEffect(() => {
    if (emailParam) setEmail(emailParam);
  }, [emailParam]);

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.top}>
        <Text style={styles.brandTx}>TX</Text>
        <Text style={styles.brandName}>TahminX</Text>
        <Text style={styles.sub}>Hesabına giriş yap</Text>
      </View>

      <View style={{ padding: spacing.xl, gap: 12 }}>
        <TxCard>
          <Text style={styles.label}>E-POSTA</Text>
          <TextInput
            value={email}
            onChangeText={setEmail}
            placeholder="ornek@mail.com"
            placeholderTextColor="#9CA3AF"
            style={styles.input}
            autoCapitalize="none"
            keyboardType="email-address"
          />

          <View style={{ height: 12 }} />

          <Text style={styles.label}>ŞİFRE</Text>
          <TextInput
            value={pass}
            onChangeText={setPass}
            placeholder="••••••••"
            placeholderTextColor="#9CA3AF"
            style={styles.input}
            secureTextEntry
          />
        </TxCard>

        <TxButton
          title="GİRİŞ YAP"
          onPress={async () => {
            const res = await loginUser({ email, password: pass });
            if (!res.ok) {
              Alert.alert("Giriş Başarısız", res.message || "Hata oluştu");
              return;
            }
            router.replace("/home");
          }}
        />

        <Pressable
          onPress={() => router.push("/register")}
          style={{ alignItems: "center", padding: 8 }}
        >
          <Text style={{ color: colors.textSecondary, fontWeight: "800" }}>
            Hesabın yok mu? <Text style={{ color: colors.primary }}>Kayıt Ol</Text>
          </Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  top: { paddingTop: 50, paddingHorizontal: spacing.xl, gap: 6 },
  brandTx: { fontSize: 28, fontWeight: "900", color: colors.textPrimary },
  brandName: { fontSize: 18, fontWeight: "900", color: colors.primary },
  sub: { color: colors.textSecondary, fontWeight: "700" },

  label: { color: "#9CA3AF", fontWeight: "900", fontSize: 12, marginBottom: 8 },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.md,
    paddingHorizontal: 12,
    paddingVertical: 12,
    fontWeight: "800",
    color: colors.textPrimary,
    backgroundColor: "#fff",
  },
});
