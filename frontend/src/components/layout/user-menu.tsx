"use client";
import useUser from "@/hooks/user";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { Button } from "../ui/button";
import UserAvatar from "../users/avatar";
import { signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import Username from "../users/username";
import RoleBadge from "../users/role-badge";
import PlayerInfo from "../users/player-info";

export default function UserMenu() {
  const { user, player } = useUser();
  const router = useRouter();
  if (!user) return;

  //@ts-ignore
  const { id, avatar, username, email, display_role } = user;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <UserAvatar className="h-8 w-8" avatar={avatar} username={username} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">
              <Username user={...user} />
              <RoleBadge {...display_role} />
            </p>
            <p className="text-xs leading-none text-muted-foreground">
              {email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem
            onClick={(e) => router.push(`/profile/${id}-${username}`)}
          >
            Profil
            <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>u
          </DropdownMenuItem>
          <DropdownMenuItem onClick={(e) => router.push("/settings")}>
            Ustawienia
            <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
          </DropdownMenuItem>
          {user.is_superuser && (
            <DropdownMenuItem onClick={(e) => router.push("/admin")}>
              Panel Admina
              <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
            </DropdownMenuItem>
          )}
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={(e) => signOut()}>
          Wyloguj się
          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
