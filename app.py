import React, { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";

// ------------------------------------------------------------
// SAT Information Dashboard - Professional Edition (Student View)
// ------------------------------------------------------------

const attempts = [
  {
    id: "A1",
    attemptLabel: "Attempt 1",
    dateLabel: "Apr 20, 2026",
    rw: 580,
    math: 640,
    total: 1220,
    rwTopics: [
      { subject: "Craft & Structure", score: 57, fullMark: 100 },
      { subject: "Info & Ideas", score: 69, fullMark: 100 },
      { subject: "Standard English", score: 77, fullMark: 100 },
      { subject: "Expression of Ideas", score: 82, fullMark: 100 },
    ],
    mathTopics: [
      { subject: "Algebra", score: 100, fullMark: 100 },
      { subject: "Problem Solving", score: 86, fullMark: 100 },
      { subject: "Advanced Math", score: 79, fullMark: 100 },
      { subject: "Additional Topics", score: 50, fullMark: 100 },
    ],
    wrongQuestions: {
      rw: [4, 12, 13, 14, 16, 19, 20, 23, 24],
      math: [11, 12, 14, 16, 19, 20, 22],
    },
  },
  // ... (Attempt 2 - 4 เหมือนเดิม)
  {
    id: "A5",
    attemptLabel: "Attempt 5",
    dateLabel: "Apr 24, 2026",
    rw: 620,
    math: 720,
    total: 1340,
    rwTopics: [
      { subject: "Craft & Structure", score: 83, fullMark: 100 },
      { subject: "Info & Ideas", score: 88, fullMark: 100 },
      { subject: "Standard English", score: 71, fullMark: 100 },
      { subject: "Expression of Ideas", score: 75, fullMark: 100 },
    ],
    mathTopics: [
      { subject: "Algebra", score: 87, fullMark: 100 },
      { subject: "Problem Solving", score: 100, fullMark: 100 },
      { subject: "Advanced Math", score: 75, fullMark: 100 },
      { subject: "Additional Topics", score: 67, fullMark: 100 },
    ],
    wrongQuestions: {
      rw: [3, 6, 10, 13, 15, 17, 20, 21, 22, 23],
      math: [10, 14, 16, 18, 19, 21, 22],
    },
  },
];

const STUDENT = {
  name: "Aphiphongphiphut Kaweeyarn",
  target: 1500,
};

export default function DigitalSATReportProfessional() {
  const latest = attempts[attempts.length - 1];
  const [selectedId, setSelectedId] = useState(latest.id);
  const selectedAttempt = useMemo(() => attempts.find(a => a.id === selectedId) || latest, [selectedId]);

  const bestTotal = Math.max(...attempts.map(a => a.total));
  const progressPercent = Math.round((bestTotal / STUDENT.target) * 100);

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10 text-slate-900">
      <div className="mx-auto max-w-7xl space-y-8">
        
        {/* Top Navigation & Info */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="h-2 w-2 rounded-full bg-sky-500 animate-pulse" />
              <span className="text-xs font-bold uppercase tracking-widest text-sky-600">Performance Hub</span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight">{STUDENT.name}</h1>
          </div>
          <div className="flex gap-3">
            <Badge variant="outline" className="bg-white px-4 py-2 text-lg font-bold border-sky-100 shadow-sm">
              🎯 Target: {STUDENT.target}
            </Badge>
            <Badge className="bg-sky-600 px-4 py-2 text-lg font-bold shadow-md shadow-sky-200">
              🏆 Best: {bestTotal}
            </Badge>
          </div>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-none shadow-xl shadow-slate-200/50">
            <CardContent className="pt-6">
              <p className="text-sm font-medium text-slate-500 mb-1">Current Progress</p>
              <div className="flex items-end justify-between mb-2">
                <span className="text-4xl font-black text-sky-600">{progressPercent}%</span>
                <span className="text-sm text-slate-400">to Goal</span>
              </div>
              <Progress value={progressPercent} className="h-3 bg-sky-100" />
            </CardContent>
          </Card>
          
          <Card className="border-none shadow-xl shadow-slate-200/50 bg-sky-600 text-white">
            <CardContent className="pt-6">
              <p className="text-sm font-medium text-sky-100 mb-1">Latest Attempt Score</p>
              <div className="text-4xl font-black">{latest.total}</div>
              <p className="text-xs text-sky-200 mt-2">{latest.dateLabel} • {latest.attemptLabel}</p>
            </CardContent>
          </Card>

          <Card className="border-none shadow-xl shadow-slate-200/50">
            <CardContent className="pt-6">
              <p className="text-sm font-medium text-slate-500 mb-1">Points Needed</p>
              <div className="text-4xl font-black text-rose-500">+{STUDENT.target - bestTotal}</div>
              <p className="text-xs text-slate-400 mt-2">to reach 1500 target</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content: Tabs for Detailed View */}
        <Tabs defaultValue="analysis" className="space-y-6">
          <TabsList className="bg-white p-1 border border-slate-200 rounded-xl h-14 shadow-sm">
            <TabsTrigger value="analysis" className="px-8 rounded-lg font-bold data-[state=active]:bg-sky-50 data-[state=active]:text-sky-600">
              Skill Analysis (Radar)
            </TabsTrigger>
            <TabsTrigger value="history" className="px-8 rounded-lg font-bold data-[state=active]:bg-sky-50 data-[state=active]:text-sky-600">
              Score History
            </TabsTrigger>
          </TabsList>

          <TabsContent value="analysis" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Radar Chart: Math */}
              <Card className="border-none shadow-lg">
                <CardHeader>
                  <CardTitle className="text-lg">Math Skill Breakdown</CardTitle>
                </CardHeader>
                <CardContent className="h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={selectedAttempt.mathTopics}>
                      <PolarGrid stroke="#e2e8f0" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                      <Radar
                        name="Math"
                        dataKey="score"
                        stroke="#0284c7"
                        fill="#0ea5e9"
                        fillOpacity={0.5}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Radar Chart: R&W */}
              <Card className="border-none shadow-lg">
                <CardHeader>
                  <CardTitle className="text-lg">Reading & Writing Skill Breakdown</CardTitle>
                </CardHeader>
                <CardContent className="h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={selectedAttempt.rwTopics}>
                      <PolarGrid stroke="#e2e8f0" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                      <Radar
                        name="R&W"
                        dataKey="score"
                        stroke="#f43f5e"
                        fill="#fb7185"
                        fillOpacity={0.5}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
            
            {/* Incorrect Questions Section */}
            <Card className="border-none shadow-lg overflow-hidden">
                <CardHeader className="bg-slate-900 text-white">
                    <CardTitle className="text-lg">Review Incorrect Questions - {selectedAttempt.attemptLabel}</CardTitle>
                </CardHeader>
                <CardContent className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-rose-500"/> Reading & Writing
                        </h4>
                        <div className="flex flex-wrap gap-2">
                            {selectedAttempt.wrongQuestions.rw.map(q => (
                                <Badge key={q} variant="secondary" className="h-10 w-10 justify-center rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100">Q{q}</Badge>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-amber-500"/> Math
                        </h4>
                        <div className="flex flex-wrap gap-2">
                            {selectedAttempt.wrongQuestions.math.map(q => (
                                <Badge key={q} variant="secondary" className="h-10 w-10 justify-center rounded-lg bg-amber-50 text-amber-600 hover:bg-amber-100">Q{q}</Badge>
                            ))}
                        </div>
                    </div>
                </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history">
            <Card className="border-none shadow-lg h-[500px] p-6">
               <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={attempts}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="attemptLabel" axisLine={false} tickLine={false} tick={{fill: '#94a3b8'}} />
                    <YAxis domain={[0, 1600]} axisLine={false} tickLine={false} tick={{fill: '#94a3b8'}} />
                    <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'}} />
                    <Legend iconType="circle" />
                    <Bar dataKey="math" name="Math" stackId="a" fill="#0ea5e9" radius={[0, 0, 0, 0]} barSize={40} />
                    <Bar dataKey="rw" name="R&W" stackId="a" fill="#f43f5e" radius={[10, 10, 0, 0]} barSize={40} />
                  </BarChart>
               </ResponsiveContainer>
          </TabsContent>
        </Tabs>

        {/* Footer Advice */}
        <div className="rounded-2xl bg-sky-50 border border-sky-100 p-6 text-center">
            <h3 className="font-bold text-sky-900 mb-2">💡 Nong Jaidee's Smart Advice</h3>
            <p className="text-sky-700">"พยายามเน้นที่หัวข้อ {selectedAttempt.mathTopics.sort((a,b)=>a.score-b.score)[0].subject} ในพาร์ท Math นะคะ เพราะเป็นจุดที่มีโอกาสเพิ่มคะแนนได้มากที่สุดค่ะ!"</p>
        </div>
      </div>
    </div>
  );
}
