import "react-native-gesture-handler";
import React from "react";
import { Drawer } from "expo-router/drawer";

import DrawerContent from "../src/navigation/DrawerContent";
import { colors } from "../src/theme/colors";
import TxHeaderBack from "../src/components/TxHeaderBack";

export default function RootLayout() {
  return (
    <Drawer
      drawerContent={(props) => <DrawerContent {...props} />}
      screenOptions={{
        headerShown: true,
        headerTitle: "TahminX",
        headerTintColor: colors.textPrimary,
        headerStyle: { backgroundColor: colors.background },
        drawerStyle: { backgroundColor: "#fff" },
      }}
    >
      {/* ✅ HOME: hamburger otomatik gelir (Drawer default) */}
      <Drawer.Screen name="home" options={{ title: "Anasayfa" }} />

      {/* ✅ Diğer sayfalar: back icon */}
      <Drawer.Screen
        name="special"
        options={{
          title: "Sana Özel Sorular",
          headerLeft: () => <TxHeaderBack />,
        }}
      />
      <Drawer.Screen
        name="ai"
        options={{
          title: "TahminX AI",
          headerLeft: () => <TxHeaderBack />,
        }}
      />
      <Drawer.Screen
        name="history"
        options={{
          title: "Soru Geçmişi",
          headerLeft: () => <TxHeaderBack />,
        }}
      />
      <Drawer.Screen
        name="profile"
        options={{
          title: "Profil",
          headerLeft: () => <TxHeaderBack />,
        }}
      />

      {/* Auth / splash menüde görünmesin */}
      <Drawer.Screen
        name="login"
        options={{ headerShown: false, drawerItemStyle: { display: "none" } }}
      />
      <Drawer.Screen
        name="register"
        options={{ headerShown: false, drawerItemStyle: { display: "none" } }}
      />
      <Drawer.Screen
        name="splash"
        options={{ headerShown: false, drawerItemStyle: { display: "none" } }}
      />

      {/* Liste/soru ekranları menüde görünmesin ama back icon olsun */}
      <Drawer.Screen
        name="questions"
        options={{
          title: "Sorular",
          drawerItemStyle: { display: "none" },
          headerLeft: () => <TxHeaderBack />,
        }}
      />
      <Drawer.Screen
        name="question"
        options={{
          title: "Soru",
          drawerItemStyle: { display: "none" },
          headerLeft: () => <TxHeaderBack />,
        }}
      />
    </Drawer>
  );
}
