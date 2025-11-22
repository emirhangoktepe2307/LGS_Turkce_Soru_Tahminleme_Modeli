"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { TrendingUp, BookOpen, Clock } from "lucide-react";

// Mock veriler - Paragrafta Anlam konusunun yıllara göre dağılımı
const yearlyData = [
  { year: "2018", count: 8 },
  { year: "2019", count: 9 },
  { year: "2020", count: 7 },
  { year: "2021", count: 10 },
  { year: "2022", count: 9 },
  { year: "2023", count: 11 },
  { year: "2024", count: 10 },
  { year: "2025", count: 9 },
  { year: "2026", count: 10, predicted: true },
];

// Mock tahmin verileri
const predictions = [
  {
    topic: "Paragrafta Yardımcı Düşünce",
    probability: 85,
    description: "Yüksek ihtimalle bu konudan soru gelecek",
  },
  {
    topic: "Paragrafta Ana Düşünce",
    probability: 78,
    description: "Geçmiş yıllarda sıkça sorulmuş",
  },
  {
    topic: "Paragrafta Anlam İlişkileri",
    probability: 72,
    description: "Orta düzeyde bir ihtimal",
  },
  {
    topic: "Cümlede Anlam İlişkileri",
    probability: 68,
    description: "Dikkat edilmesi gereken bir konu",
  },
];

// Mock son çözülen sorular
const recentQuestions = [
  {
    id: 1,
    topic: "Paragrafta Ana Düşünce",
    date: "2025-11-22",
    time: "14:30",
    result: "Doğru",
    difficulty: "Orta",
  },
  {
    id: 2,
    topic: "Paragrafta Yardımcı Düşünce",
    date: "2025-11-22",
    time: "14:15",
    result: "Yanlış",
    difficulty: "Zor",
  },
  {
    id: 3,
    topic: "Cümlede Anlam İlişkileri",
    date: "2025-11-21",
    time: "16:45",
    result: "Doğru",
    difficulty: "Kolay",
  },
  {
    id: 4,
    topic: "Paragrafta Anlam İlişkileri",
    date: "2025-11-21",
    time: "15:20",
    result: "Doğru",
    difficulty: "Orta",
  },
  {
    id: 5,
    topic: "Paragrafta Ana Düşünce",
    date: "2025-11-20",
    time: "13:10",
    result: "Yanlış",
    difficulty: "Zor",
  },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Başlık */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">LGS hazırlık durumunuz ve tahminleriniz</p>
      </div>

      {/* Grafik Bölümü */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-primary-600" />
            Paragrafta Anlam Konusunun Yıllara Göre Dağılımı
          </CardTitle>
          <CardDescription>
            2018-2026 yılları arası soru sayıları ve 2026 tahmini
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={yearlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="year" 
                stroke="#6b7280"
                tick={{ fill: "#6b7280" }}
              />
              <YAxis 
                stroke="#6b7280"
                tick={{ fill: "#6b7280" }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: "#fff", 
                  border: "1px solid #e5e7eb",
                  borderRadius: "8px"
                }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="count" 
                stroke="#3b82f6" 
                strokeWidth={2}
                name="Soru Sayısı"
                dot={{ fill: "#3b82f6", r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-sm text-gray-500 mt-4 text-center">
            * 2026 yılı tahmini veridir
          </p>
        </CardContent>
      </Card>

      {/* 2026 Tahmini Kartı */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-primary-600" />
            2026 Tahmini Soru Tipleri
          </CardTitle>
          <CardDescription>
            Yapay zeka analizine göre 2026 LGS'de çıkma ihtimali yüksek konular
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {predictions.map((prediction, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4 bg-gradient-to-br from-blue-50 to-white hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-gray-900">
                    {prediction.topic}
                  </h3>
                  <span className="text-2xl font-bold text-primary-600">
                    %{prediction.probability}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all"
                    style={{ width: `${prediction.probability}%` }}
                  />
                </div>
                <p className="text-sm text-gray-600">{prediction.description}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Son Çözülen Sorular */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-6 h-6 text-primary-600" />
            Son Çözülen Sorular
          </CardTitle>
          <CardDescription>
            Son çözdüğünüz soruların listesi ve sonuçları
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recentQuestions.map((question) => (
              <div
                key={question.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="font-medium text-gray-900">
                      {question.topic}
                    </h3>
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        question.result === "Doğru"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {question.result}
                    </span>
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        question.difficulty === "Kolay"
                          ? "bg-blue-100 text-blue-700"
                          : question.difficulty === "Orta"
                          ? "bg-yellow-100 text-yellow-700"
                          : "bg-orange-100 text-orange-700"
                      }`}
                    >
                      {question.difficulty}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">
                    {question.date} - {question.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

