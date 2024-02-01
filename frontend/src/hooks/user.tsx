"use client";
import { useSession } from "next-auth/react";

export default function useUser() {
  const { data: session, status } = useSession();

  function hasScope(roles: any, scope: string) {
    let has = false;
    roles.map((role) => {
      role.scopes.map((item) => {
        const scopeSplit = scope.split(":");
        const app_name = scopeSplit[0];
        const value = scopeSplit[1];
        if (item.app_name == app_name && item.value == value) {
          has = true;
        }
      });
    });

    return has;
  }

  function hasRole(display_role: any, roles: any, roleTag: string) {
    if (display_role?.tag == roleTag) {
      return true;
    }
    let has = false;
    roles?.map((item) => {
      if (item.tag == roleTag) {
        has = true;
      }
    });

    return has;
  }

  function isAuthor(resourceId: number) {
    return session?.user.id === resourceId;
  }

  function isVip() {
    return hasRole(session?.user?.display_role, session?.user?.roles, "vip");
  }

  function isSuperUser() {
    return session?.user.is_superuser;
  }

  return {
    user: session?.user,
    player: session?.user?.player,
    steamrep_profile: session?.user?.player?.steamrep_profile,
    access_token: session?.access_token,
    refresh_token: session?.refresh_token,
    status: status,
    authenticated: status === "authenticated",
    hasScope: hasScope,
    hasRole: hasRole,
    isAuthor: isAuthor,
    isSuperUser: isSuperUser,
    isVip: isVip,
  };
}
