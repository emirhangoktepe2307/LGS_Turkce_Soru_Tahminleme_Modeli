import React from "react";
import { Redirect } from "expo-router";

export default function Index() {
  // RootLayout mount olduktan sonra güvenli yönlendirir
  return <Redirect href="/register" />;
}
