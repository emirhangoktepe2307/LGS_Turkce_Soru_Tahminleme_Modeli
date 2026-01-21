import AsyncStorage from "@react-native-async-storage/async-storage";

const AUTH_KEY = "TAHMINX_AUTH_V2"; // { loggedIn: boolean, user: {name,email} }
const USER_KEY = "TAHMINX_USER_V2"; // { name,email,password }

export async function getSavedUser() {
  const raw = await AsyncStorage.getItem(USER_KEY);
  return raw ? JSON.parse(raw) : null;
}

export async function registerUser({ name, email, password }) {
  const user = {
    name: String(name || "").trim(),
    email: String(email || "").trim(),
    password: String(password || "").trim(),
  };

  await AsyncStorage.setItem(USER_KEY, JSON.stringify(user));

  // kayıt olunca otomatik giriş YOK
  await AsyncStorage.removeItem(AUTH_KEY);

  return { name: user.name, email: user.email };
}

export async function loginUser({ email, password }) {
  const saved = await getSavedUser();
  if (!saved) return { ok: false, message: "Kayıt bulunamadı. Önce kayıt ol." };

  const e = String(email || "").trim();
  const p = String(password || "").trim();

  if (saved.email !== e || saved.password !== p) {
    return { ok: false, message: "E-posta veya şifre hatalı." };
  }

  await AsyncStorage.setItem(
    AUTH_KEY,
    JSON.stringify({ loggedIn: true, user: { name: saved.name, email: saved.email } })
  );

  return { ok: true, user: { name: saved.name, email: saved.email } };
}

export async function isLoggedIn() {
  const raw = await AsyncStorage.getItem(AUTH_KEY);
  if (!raw) return false;
  try {
    const obj = JSON.parse(raw);
    return obj?.loggedIn === true;
  } catch {
    return false;
  }
}

export async function getCurrentUser() {
  const raw = await AsyncStorage.getItem(AUTH_KEY);
  if (!raw) return null;
  try {
    const obj = JSON.parse(raw);
    return obj?.user || null;
  } catch {
    return null;
  }
}

export async function logoutUser() {
  await AsyncStorage.removeItem(AUTH_KEY);
}
