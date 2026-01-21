import React, { useState } from "react";
import { View, Text, StyleSheet, TextInput, Pressable, Alert } from "react-native";
import { router } from "expo-router";

import TxCard from "../src/components/TxCard";
import TxButton from "../src/components/TxButton";
import { colors } from "../src/theme/colors";
import { spacing } from "../src/theme/spacing";
import { radius } from "../src/theme/radius";
import { registerUser } from "../src/utils/auth";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <View style={styles.top}>
        <Text style={styles.title}>Kayıt Ol</Text>
        <Text style={styles.sub}>TahminX hesabını oluştur</Text>
      </View>

      <View style={{ padding: spacing.xl, gap: 12 }}>
        <TxCard>
          <Text style={styles.label}>AD SOYAD</Text>
          <TextInput
            value={name}
            onChangeText={setName}
            placeholder="Ad Soyad"
            placeholderTextColor="#9CA3AF"
            style={styles.input}
          />

          <View style={{ height: 12 }} />

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
          title="KAYIT OL"
          onPress={async () => {
            const n = name.trim();
            const e = email.trim();
            const p = pass.trim();

            if (!n || !e || !p) {
              Alert.alert("Uyarı", "Lütfen tüm alanları doldur.");
              return;
            }
            if (!e.includes("@")) {
              Alert.alert("Uyarı", "Geçerli bir e-posta gir.");
              return;
            }
            if (p.length < 6) {
              Alert.alert("Uyarı", "Şifre en az 6 karakter olmalı.");
              return;
            }

            await registerUser({ name: n, email: e, password: p });

            Alert.alert("Başarılı", "Kayıt oluşturuldu. Giriş yapabilirsin.");
            router.replace(`/login?email=${encodeURIComponent(e)}`);
          }}
        />

        <Pressable onPress={() => router.replace("/login")} style={{ alignItems: "center", padding: 8 }}>
          <Text style={{ color: colors.textSecondary, fontWeight: "800" }}>
            Zaten hesabın var mı? <Text style={{ color: colors.primary }}>Giriş Yap</Text>
          </Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  top: { paddingTop: 50, paddingHorizontal: spacing.xl, gap: 6 },
  title: { fontSize: 22, fontWeight: "900", color: colors.textPrimary },
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
