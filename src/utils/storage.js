import AsyncStorage from "@react-native-async-storage/async-storage";

const HISTORY_KEY = "TAHMINX_HISTORY_V3";

// ✅ Eski sürümlerde kullanmış olabileceğin key'leri de dene
const LEGACY_KEYS = ["TAHMINX_HISTORY_V2", "TAHMINX_HISTORY", "HISTORY_KEY"];

function safeParse(raw, fallback) {
  try {
    const v = JSON.parse(raw);
    return v ?? fallback;
  } catch {
    return fallback;
  }
}

function normalizeType(t) {
  const x = String(t || "").toLowerCase();
  if (x.includes("cumle")) return "cumle";
  if (x.includes("parag")) return "paragraf";
  return x || "cumle";
}

function makeId() {
  return `h-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function normalizeEntry(it) {
  // Eski kayıtlardan gelenleri de bu formata sok
  const date = it?.date || it?.createdAt || it?.time || new Date().toISOString();
  const successRaw = it?.success ?? it?.score ?? it?.result ?? 0;
  const success = Number(successRaw) >= 50 ? 100 : Number(successRaw) === 100 ? 100 : 0;

  return {
    id: String(it?.id || makeId()),
    qid: String(it?.qid || it?.questionId || it?.qId || it?.idQ || ""),
    type: normalizeType(it?.type || it?.mode),
    topic: String(it?.topic || it?.subject || "Konu"),
    year: String(it?.year || it?.yil || "-"),
    success,
    date: String(date),
  };
}

async function readAnyHistory() {
  // 1) Yeni key
  const rawNew = await AsyncStorage.getItem(HISTORY_KEY);
  const newList = rawNew ? safeParse(rawNew, []) : [];
  if (Array.isArray(newList) && newList.length) return newList;

  // 2) Legacy key'ler
  for (const k of LEGACY_KEYS) {
    const raw = await AsyncStorage.getItem(k);
    const list = raw ? safeParse(raw, []) : [];
    if (Array.isArray(list) && list.length) return list;
  }

  return [];
}

export async function getHistory() {
  const list = await readAnyHistory();
  const normalized = (Array.isArray(list) ? list : [])
    .map(normalizeEntry)
    .filter((x) => x.qid); // qid yoksa çöpe

  // ✅ migrate: yeni key'e yaz
  await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify(normalized));

  // en yeni üstte
  return normalized.sort((a, b) => new Date(b?.date || 0) - new Date(a?.date || 0));
}

export async function clearHistory() {
  await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify([]));
}

export async function addHistoryEntry({
  qid,
  type,
  topic,
  year,
  success,
  date = new Date().toISOString(),
}) {
  if (!qid) return;

  const entry = normalizeEntry({
    id: makeId(),
    qid,
    type,
    topic,
    year,
    success,
    date,
  });

  const list = await getHistory();

  // çift kayıt önleme
  const last = list[0];
  if (last && String(last.qid) === entry.qid) {
    const dt = Math.abs(new Date(entry.date) - new Date(last.date));
    if (dt < 1500) return;
  }

  const updated = [entry, ...list].slice(0, 300);
  await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
}
