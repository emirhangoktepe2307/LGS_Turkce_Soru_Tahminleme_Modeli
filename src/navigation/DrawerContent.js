// src/navigation/DrawerContent.js
import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { DrawerContentScrollView } from "@react-navigation/drawer";
import { router, usePathname } from "expo-router";

import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { radius } from "../theme/radius";
import { logoutUser, getCurrentUser } from "../utils/auth";

const MenuItem = ({ icon, label, active, onPress }) => (
  <Pressable
    onPress={onPress}
    style={({ pressed }) => [
      styles.item,
      active && styles.itemActive,
      pressed && { opacity: 0.92 },
    ]}
  >
    <Text style={[styles.icon, active && styles.iconActive]}>{icon}</Text>
    <Text style={[styles.itemText, active && styles.itemTextActive]}>
      {label}
    </Text>
  </Pressable>
);

export default function DrawerContent(props) {
  const pathname = usePathname(); // "/home" "/ai" vs
  const [user, setUser] = useState(null);

  useEffect(() => {
    let mounted = true;
    getCurrentUser().then((u) => {
      if (mounted) setUser(u);
    });
    return () => {
      mounted = false;
    };
  }, [pathname]);

  const go = (to) => {
    props.navigation.closeDrawer();
    router.push(to);
  };

  const logout = async () => {
    await logoutUser();
    props.navigation.closeDrawer();
    router.replace("/login");
  };

  const isActive = (path) => pathname === path;

  const initials = (user?.name || "U")
    .trim()
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((x) => x[0]?.toUpperCase())
    .join("");

  return (
    <DrawerContentScrollView
      {...props}
      contentContainerStyle={styles.container}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{initials || "U"}</Text>
        </View>

        <View style={{ flex: 1 }}>
          <Text style={styles.userName}>{user?.name || "Misafir"}</Text>
          <Text style={styles.userMail}>{user?.email || "—"}</Text>
        </View>
      </View>

      <View style={styles.brandRow}>
        <Text style={styles.brandTx}>TX</Text>
        <Text style={styles.brandName}>TahminX</Text>
      </View>
      <Text style={styles.brandSub}>LGS Türkçe • Yapay Zeka</Text>

      <View style={{ height: 18 }} />

      {/* Menü */}
      <MenuItem
        icon="🏠"
        label="Anasayfa"
        active={isActive("/home")}
        onPress={() => go("/home")}
      />
      <MenuItem
        icon="✨"
        label="Sana Özel Sorular"
        active={isActive("/special")}
        onPress={() => go("/special")}
      />
      <MenuItem
        icon="🤖"
        label="TahminX AI"
        active={isActive("/ai")}
        onPress={() => go("/ai")}
      />
      <MenuItem
        icon="📚"
        label="Soru Geçmişi"
        active={isActive("/history")}
        onPress={() => go("/history")}
      />
      <MenuItem
        icon="👤"
        label="Profil"
        active={isActive("/profile")}
        onPress={() => go("/profile")}
      />

      <View style={{ flex: 1 }} />

      {/* Çıkış */}
      <Pressable
        onPress={logout}
        style={({ pressed }) => [styles.logout, pressed && { opacity: 0.92 }]}
      >
        <Text style={styles.logoutText}>Çıkış Yap</Text>
      </Pressable>

      <Text style={styles.footer}>© TahminX</Text>
    </DrawerContentScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: spacing.xl,
    paddingBottom: 24,
    flexGrow: 1,
    backgroundColor: "#fff",
  },

  header: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingTop: 6,
    paddingBottom: 10,
  },
  avatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "rgba(239,68,68,0.15)",
    alignItems: "center",
    justifyContent: "center",
  },
  avatarText: { fontWeight: "900", color: colors.primary, fontSize: 16 },
  userName: { fontWeight: "900", color: colors.textPrimary, fontSize: 16 },
  userMail: { marginTop: 2, color: colors.textSecondary, fontWeight: "700" },

  brandRow: { flexDirection: "row", alignItems: "center", gap: 8, marginTop: 6 },
  brandTx: { fontSize: 22, fontWeight: "900", color: colors.textPrimary },
  brandName: { fontSize: 18, fontWeight: "900", color: colors.primary },
  brandSub: { marginTop: 6, color: colors.textSecondary, fontWeight: "700" },

  item: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingVertical: 12,
    paddingHorizontal: 12,
    borderRadius: radius.md,
    marginBottom: 8,
  },
  itemActive: { backgroundColor: "rgba(239,68,68,0.12)" },
  icon: { fontSize: 16 },
  iconActive: { opacity: 1 },
  itemText: { fontWeight: "900", color: colors.textPrimary },
  itemTextActive: { color: colors.primary },

  logout: {
    marginTop: 14,
    backgroundColor: colors.textPrimary,
    paddingVertical: 12,
    borderRadius: radius.md,
    alignItems: "center",
  },
  logoutText: { color: "#fff", fontWeight: "900" },
  footer: {
    marginTop: 14,
    color: colors.textSecondary,
    fontWeight: "700",
    textAlign: "center",
  },
});
