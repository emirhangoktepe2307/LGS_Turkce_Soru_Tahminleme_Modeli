import { topicsCumle, topicsParagraf } from "./topics";
import { years } from "./stats";

// ---------- helpers ----------
const slug = (s) =>
  String(s)
    .toLowerCase()
    .replace(/ğ/g, "g")
    .replace(/ü/g, "u")
    .replace(/ş/g, "s")
    .replace(/ı/g, "i")
    .replace(/ö/g, "o")
    .replace(/ç/g, "c")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");

const topicToString = (t) => {
  if (t == null) return "";
  if (typeof t === "string") return t;
  if (typeof t === "object") return String(t.label || t.title || t.name || t.value || "");
  return String(t);
};

function hashSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function seededPick(arr, seed) {
  if (!Array.isArray(arr) || arr.length === 0) return undefined;
  return arr[seed % arr.length];
}

function seededShuffle(arr, seed) {
  const a = Array.isArray(arr) ? [...arr] : [];
  let s = seed >>> 0;
  for (let i = a.length - 1; i > 0; i--) {
    s = (s * 1664525 + 1013904223) >>> 0;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function takeDeterministicSubset(list, count, seed) {
  const arr = seededShuffle((list || []).map(topicToString).filter(Boolean), seed);
  return arr.slice(0, Math.max(0, count));
}

// ---------- variation pools (farklı görünüm için) ----------
const cumleStems = [
  "Aşağıdaki cümlelerin hangisinde",
  "Aşağıdaki seçeneklerin hangisinde",
  "Verilen cümlelerden hangisinde",
  "Aşağıdakilerden hangisinde",
];

const cumleTargets = [
  { key: "neden", text: "neden-sonuç ilişkisi vardır?", correct: "Yoğun çalıştığı için sınavı kazandı." },
  { key: "amac", text: "amaç-sonuç ilişkisi vardır?", correct: "Daha iyi anlamak için not tuttu." },
  { key: "kosul", text: "koşul anlamı vardır?", correct: "Düzenli tekrar yaparsan ilerlersin." },
  { key: "kars", text: "karşılaştırma yapılmıştır?", correct: "Bu deneme, önceki denemeden daha zordu." },
];

const cumleWrongsPool = [
  "Sabah erkenden okula gitti.",
  "Defterini çantasına koydu.",
  "Kitabı masanın üstüne bıraktı.",
  "Ödevini akşam bitirdi.",
  "Pencereden dışarı baktı.",
  "Arkadaşıyla telefonla konuştu.",
  "Bahçede biraz yürüdü.",
  "Dersi dikkatle dinledi.",
];

const paragrafOpeners = [
  "Son yıllarda öğrencilerin çalışma alışkanlıkları değişti.",
  "Günlük yaşamda küçük tercihler büyük sonuçlar doğurabilir.",
  "Bir işi iyi yapmak, o işe düzenli zaman ayırmayı gerektirir.",
  "Başarı, çoğu zaman küçük adımların birikimidir.",
];

const paragrafMiddles = [
  "Özellikle {topic} ile ilgili sorularda, metni dikkatle okumak gerekir.",
  "{topic} konusunu anlamak için cümleler arasındaki bağı görmek önemlidir.",
  "{topic} sorularında anahtar kelimeler, düşünceyi yakalamayı kolaylaştırır.",
  "{topic} çalışırken örnekler üzerinden ilerlemek kalıcı öğrenme sağlar.",
];

const paragrafClosers = [
  "Bu yüzden öğrenci, acele etmeden metni çözümlemeli ve doğru seçeneği aramalıdır.",
  "Bu yaklaşım, yalnızca sınavda değil günlük hayatta da daha doğru yorum yapmayı sağlar.",
  "Böylece kişi, parçaları birleştirerek metnin asıl mesajını daha rahat kavrar.",
  "Sonuç olarak düzenli pratik, konuya hakimiyeti belirgin biçimde artırır.",
];

const paragrafQPool = [
  {
    q: "Bu paragrafın ana düşüncesi aşağıdakilerden hangisidir?",
    correct: "Düzenli ve dikkatli çalışma, anlamayı güçlendirir.",
    wrongs: [
      "Sınavlar her zaman kolaydır.",
      "Okumak gereksiz bir uğraştır.",
      "Başarı tamamen şansa bağlıdır.",
    ],
  },
  {
    q: "Bu paragraftan çıkarılabilecek en uygun sonuç aşağıdakilerden hangisidir?",
    correct: "Metni doğru çözümlemek için dikkat ve pratik gerekir.",
    wrongs: [
      "Hızlı okumak her zaman yeterlidir.",
      "Soruların tamamı aynı yöntemle çözülür.",
      "Konu çalışmaya gerek yoktur.",
    ],
  },
  {
    q: "Bu paragrafta vurgulanmak istenen aşağıdakilerden hangisidir?",
    correct: "Doğru yoruma ulaşmak için parçalar arasındaki ilişki önemlidir.",
    wrongs: [
      "Sadece ezber yapanlar başarılı olur.",
      "Soru çözmek zaman kaybıdır.",
      "Her metin aynı mesajı verir.",
    ],
  },
];

// ---------- generators ----------
function makeCumleQuestion(topicRaw, year) {
  const topic = topicToString(topicRaw) || "Cümlede Anlam";
  const seed = hashSeed(`${topic}|${year}|cumle`);

  const stem = seededPick(cumleStems, seed) || cumleStems[0];
  const target = seededPick(cumleTargets, seed ^ 77) || cumleTargets[0];

  // wrongs: havuzdan seed'e göre seç
  const wrongs = seededShuffle(cumleWrongsPool, seed ^ 999).slice(0, 3);

  // correct cümleyi topic+yıl ile farklılaştır
  const correct = target.correct;


  const choices = seededShuffle([correct, ...wrongs], seed);
  const answerIndex = choices.indexOf(correct);

  return {
    id: `c-${slug(topic)}-${year}`,
    type: "cumle",
    topic,
    year: String(year),
    passage: null,
    question: `${topic} (${year}): ${stem} ${target.text}`,
    choices,
    answerIndex: Math.max(0, answerIndex),
  };
}

function makeParagrafQuestion(topicRaw, year) {
  const topic = topicToString(topicRaw) || "Paragrafta Anlam";
  const seed = hashSeed(`${topic}|${year}|paragraf`);

  const opener = seededPick(paragrafOpeners, seed) || paragrafOpeners[0];
  const middleTpl = seededPick(paragrafMiddles, seed ^ 13) || paragrafMiddles[0];
  const closer = seededPick(paragrafClosers, seed ^ 31) || paragrafClosers[0];

  const middle = middleTpl.replace("{topic}", topic);

  // Paragrafı yıl ile de farklılaştır
  const passage = `${opener} ${middle} (${year}). ${closer}`;

  const pq = seededPick(paragrafQPool, seed ^ 12345) || paragrafQPool[0];

  const correct = pq.correct; 
  const choices = seededShuffle([correct, ...pq.wrongs], seed);
  const answerIndex = choices.indexOf(correct);

  return {
    id: `p-${slug(topic)}-${year}`,
    type: "paragraf",
    topic,
    year: String(year),
    passage,
    question: `${topic} (${year}): ${pq.q}`,
    choices,
    answerIndex: Math.max(0, answerIndex),
  };
}

// ---------- IMPORTANT: sayı düşürme ----------
const safeYears =
  Array.isArray(years) && years.length ? years.map(String) : ["2025"];

// ✅ sadece son 3 yıl (daha az soru)
const pickedYears = safeYears.slice(0, 3);

// ✅ her tür için sadece 6 topic (daha az soru)
const pickedCumleTopics = takeDeterministicSubset(topicsCumle, 6, 111);
const pickedParagrafTopics = takeDeterministicSubset(topicsParagraf, 6, 222);

export const mockQuestions = [
  ...pickedYears.flatMap((y) => pickedCumleTopics.map((t) => makeCumleQuestion(t, y))),
  ...pickedYears.flatMap((y) => pickedParagrafTopics.map((t) => makeParagrafQuestion(t, y))),
];
