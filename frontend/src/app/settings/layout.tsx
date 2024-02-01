import SettingsLayout from "@/components/settings/layout"
import { Metadata } from "next"
import { getServerSession } from "next-auth/next"
import Image from "next/image"
import { authOptions } from "../api/auth/[...nextauth]/route"
import { redirect } from 'next/navigation'


export const metadata: Metadata = {
    title: "Forms",
    description: "Advanced form example using react-hook-form and Zod.",
}

interface SettingsLayoutProps {
    children: React.ReactNode
}

export default async function SettingsLayoutPage({ children }: SettingsLayoutProps) {
    const session = await getServerSession(authOptions);
    if (!session) {
        return redirect("/auth/login")
    }
    return (
        <>
            <SettingsLayout>{children}</SettingsLayout>
        </>
    )
}