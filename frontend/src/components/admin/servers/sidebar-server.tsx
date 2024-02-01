import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {}

const sidebarNavItems = [
  {
    name: "Użytkownicy",
    icon: <Users className="h-6 w-6" />,
    links: [
      {
        title: "Lista użytkowników",
        href: "/admin/users",
      },
      {
        title: "Dodaj użytkownika",
        href: "/admin/users/create",
      },
    ],
  },
  {
    name: "Role",
    icon: <Users className="h-6 w-6" />,
    links: [
      {
        title: "Lista ról",
        href: "/admin/roles",
      },
      {
        title: "Dodaj role",
        href: "/admin/roles/create",
      },
    ],
  },
  {
    name: "Gracze",
    links: [
      {
        title: "Lista graczy",
        href: "/admin/players",
      },
    ],
  },
  {
    name: "Serwery",
    links: [
      {
        title: "Lista serwerow",
        href: "/admin/servers",
      },
      {
        title: "Dodaj serwer",
        href: "/admin/servers/create",
      },
    ],
  },
  {
    name: "Forum",
    links: [
      {
        title: "Lista kategorii",
        href: "/admin/forum-categories",
      },
      {
        title: "Dodaj kategorie",
        href: "/admin/forum-categories/create",
      },
    ],
  },
];

export function ServerSidebar({ className }: SidebarProps) {
  const router = useRouter();
  const pathname = usePathname();
  return (
    <div className={cn("pb-12", className)}>
      <div className="space-y-4 py-4">
        <div className="px-3 py-2">
          {sidebarNavItems.map((item) => (
            <div key={item.name}>
              <div className="flex">
                <div className="mr-2">{item.icon}</div>
                <div>
                  <h2 className="text-lg font-semibold tracking-tight">
                    {item.name}
                  </h2>
                </div>
              </div>
              <div className="space-y-1">
                {item.links.map((link) => (
                  <Button
                    key={link.href}
                    variant={pathname === link.href ? "secondary" : "ghost"}
                    className="w-full justify-start"
                    onClick={() => router.push(link.href)}
                  >
                    {link.title}
                  </Button>
                ))}
              </div>
              <Separator className="mt-2 mb-2" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
