"use client";
import { Separator } from "@/components/ui/separator";
import { SidebarNav } from "@/components/settings/sidebar-nav";
import { Sidebar } from "./sidebar";

interface SettingsLayoutProps {
  children: React.ReactNode;
}

export default function AdminLayout({ children }: SettingsLayoutProps) {
  return (
    <div className="grid lg:grid-cols-5">
      <Sidebar className=" lg:block" />
      <div className="col-span-3 lg:col-span-4 lg:border-l">
        <div className="h-full px-4 py-6 lg:px-8">{children}</div>
      </div>
    </div>
  );
}
