"use client";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ServerSidebar } from "./sidebar-server";
import React, { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

interface SettingsLayoutProps {
  children: React.ReactNode;
}

let tabs = [
  {
    name: "Informacje o serwerze",
    value: "details",
  },
  {
    name: "Grupy",
    value: "groups",
  },
  {
    name: "Administratorzy",
    value: "admins",
  },
];

export default function AdminServerLayout({ children }: SettingsLayoutProps) {
  const searchParams = useSearchParams();
  const [tabValue, setTabValue] = React.useState("details");
  const tab = searchParams.get("tab") || "details";
  useEffect(() => {
    setTabValue(tab);
  }, [tab]);
  const router = useRouter();
  return (
    <div className="grid lg:grid-cols-1">
      <Tabs defaultValue="details" value={tabValue} onValueChange={setTabValue}>
        <TabsList>
          {tabs.map((tab) => (
            <TabsTrigger
              key={tab.value}
              value={tab.value}
              onClick={() => router.push(`?tab=${tab.value}`)}
            >
              {tab.name}
            </TabsTrigger>
          ))}
        </TabsList>
        <div className="col-span-3 lg:col-span-4 lg:border-l">
          <div className="h-full px-4 py-6 lg:px-8">
            <TabsContent value={tab}>{children}</TabsContent>
          </div>
        </div>
      </Tabs>
    </div>
  );
}
