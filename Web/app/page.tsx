"use client";

import { ArrowRight, Brain, Target, TrendingUp, BookOpen, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Hero Bölümü */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            LGS 2026 Türkçe Sorularını
            <span className="block text-primary-600 mt-2">Şimdiden Keşfet</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed">
            Geçmiş verilerle geleceği tahmin eden yapay zeka destekli asistan
          </p>
          <Link href="/dashboard">
            <Button size="lg" className="text-lg px-8 py-6 h-auto group">
              Hemen Başla
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Özellikler Bölümü */}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Neden Bu Asistan?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            LGS hazırlığınızı bir üst seviyeye taşıyın
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Kart 1: Akıllı Soru Tahmini */}
          <Card className="border-2 border-transparent hover:border-primary-200 transition-all hover:shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <Brain className="w-6 h-6 text-primary-600" />
              </div>
              <CardTitle className="text-2xl mb-2">Akıllı Soru Tahmini</CardTitle>
              <CardDescription className="text-base">
                2018-2025 yılları arasındaki tüm çıkmış soruları analiz ederek 2026 sınavı için tahminler yapıyoruz
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>8 yıllık veri analizi</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Makine öğrenmesi algoritmaları</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Yüksek doğruluk oranı</span>
                </li>
              </ul>
            </CardContent>
          </Card>

          {/* Kart 2: Kazanım Odaklı Çalışma */}
          <Card className="border-2 border-transparent hover:border-primary-200 transition-all hover:shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-primary-600" />
              </div>
              <CardTitle className="text-2xl mb-2">Kazanım Odaklı Çalışma</CardTitle>
              <CardDescription className="text-base">
                Sadece Paragrafta Anlam ve Cümlede Anlam konularına odaklanarak verimli çalışın
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>MEB kazanımlarına uygun</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Hedefli konu seçimi</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Zaman tasarrufu</span>
                </li>
              </ul>
            </CardContent>
          </Card>

          {/* Kart 3: Hata Analizi */}
          <Card className="border-2 border-transparent hover:border-primary-200 transition-all hover:shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-primary-600" />
              </div>
              <CardTitle className="text-2xl mb-2">Hata Analizi</CardTitle>
              <CardDescription className="text-base">
                Ezberletmez, öğretir. Yanlış yaptığınız soruların nedenlerini anlayın ve gelişin
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Detaylı açıklamalar</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Öğrenme yol haritası</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">✓</span>
                  <span>Kişiselleştirilmiş geri bildirim</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Hakkında Bölümü */}
      <section className="bg-white border-t border-gray-200">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <BookOpen className="w-8 h-8 text-primary-600" />
              </div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Hakkında
              </h2>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-white rounded-2xl p-8 md:p-12 border border-gray-100 shadow-sm">
              <div className="space-y-6 text-gray-700 leading-relaxed">
                <p className="text-lg md:text-xl">
                  Bu proje, <strong className="text-gray-900">LGS 2026 Türkçe sınav sorularını tahmin etmek</strong> amacıyla geliştirilmiş bir okul projesidir.
                </p>
                
                <p>
                  Proje kapsamında, <strong className="text-gray-900">2018-2025 yılları arasındaki tüm LGS çıkmış soruları</strong> MEB kazanımlarına göre etiketlenmiş ve makine öğrenmesi algoritmaları ile analiz edilmiştir. Sistem, özellikle <strong className="text-gray-900">Paragrafta Anlam</strong> ve <strong className="text-gray-900">Cümlede Anlam</strong> konularına odaklanmaktadır.
                </p>

                <p>
                  Amacımız, öğrencilerin sadece soru çözmelerini değil, <strong className="text-gray-900">yanlış yaptıkları soruların nedenlerini anlamalarını</strong> ve bu sayede gerçek anlamda öğrenmelerini sağlamaktır. Sistem, ezberletmek yerine öğretmeyi hedefler ve her soru için detaylı açıklamalar ve öğrenme yol haritaları sunar.
                </p>

                <div className="flex items-center gap-2 text-primary-600 pt-4 border-t border-gray-200">
                  <Users className="w-5 h-5" />
                  <span className="font-medium">Eğitim odaklı, öğrenci dostu yaklaşım</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-2xl font-bold mb-4">LGS Analiz ve Tahmin Asistanı</h3>
          <p className="text-gray-400 mb-6">
            Geleceği tahmin etmek için geçmişi analiz ediyoruz
          </p>
          <p className="text-sm text-gray-500">
            © 2025 - Okul Projesi
          </p>
        </div>
      </footer>
    </div>
  );
}
