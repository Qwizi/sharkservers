'use client'
import { Separator } from "@/components/ui/separator"
import { SidebarNav } from "@/components/settings/sidebar-nav"

const sidebarNavItems = [
    {
        title: "Nazwa użytkownika",
        href: "/settings",
    },
    {
        title: "E-mail",
        href: "/settings/email",
    },
    {
        title: "Hasło",
        href: "/settings/password",
    },
    {
        title: "Avatar",
        href: "/settings/avatar",
    },
    {
        title: "Zarządzaj subscrybcja",
        href: "/settings/subscription",
    },
    {
        title: "Połaczone konta",
        href: "/settings/connected-accounts"
    }
]

interface SettingsLayoutProps {
    children: React.ReactNode
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
    return (
        <div className="rounded-[0.5rem] border bg-background shadow">
            <div className="space-y-6 p-10 pb-16 md:block">
                <div className="space-y-0.5">
                    <h2 className="text-2xl font-bold tracking-tight">Ustawienia</h2>
                    <p className="text-muted-foreground">
                        Zarządzaj twoim kontem
                    </p>
                </div>
                <Separator />
                <div className="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
                    <aside className="-mx-4 lg:w-1/4 flex-wrap">
                        <SidebarNav items={sidebarNavItems} />
                    </aside>
                    <div className="flex-1 lg:max-w-2xl">{children}</div>
                </div>
            </div>
        </div>
    )
}