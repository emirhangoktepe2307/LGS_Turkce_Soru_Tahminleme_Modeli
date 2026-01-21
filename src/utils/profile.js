import AsyncStorage from "@react-native-async-storage/async-storage";

const PROFILE_KEY = "TAHMINX_PROFILE_STATS";

const defaultStats = {
  totalSolved: 0,
  correct: 0,
  wrong: 0,
};

export async function getProfileStats() {
  const raw = await AsyncStorage.getItem(PROFILE_KEY);
  if (!raw) return defaultStats;
  try {
    return JSON.parse(raw);
  } catch {
    return defaultStats;
  }
}

export async function updateProfileStats(isCorrect) {
  const current = await getProfileStats();

  const updated = {
    totalSolved: current.totalSolved + 1,
    correct: current.correct + (isCorrect ? 1 : 0),
    wrong: current.wrong + (isCorrect ? 0 : 1),
  };

  await AsyncStorage.setItem(PROFILE_KEY, JSON.stringify(updated));
  return updated;
}

export async function resetProfileStats() {
  await AsyncStorage.setItem(PROFILE_KEY, JSON.stringify(defaultStats));
}
