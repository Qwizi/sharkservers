"use client";
import { useSession } from "next-auth/react";
import { Button } from "../ui/button";
import { Separator } from "../ui/separator";
import useApi from "@/hooks/api";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export function RefreshSessionTab() {
  const { data: session, update, status } = useSession();
  const [dataRefreshed, setDataRefreshed] = useState(false);
  const api = useApi();
  const router = useRouter();
  async function refreshSession() {
    if (status === "unauthenticated") return;
    if (dataRefreshed) return;
    try {
      const userData = await api.usersMe.getLoggedUser();
      console.log(userData);
      await update({
        ...session,
        user: {
          ...session?.user,
          ...userData,
        },
      });
      setDataRefreshed(true);
    } catch (e) {
      console.error(e);
    } finally {
      router.push("/settings");
    }
  }

  useEffect(() => {
    refreshSession().catch((e) => console.error(e));
  }, [session, status]);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">Odśwież sesje</h3>
        <p className="text-sm text-muted-foreground">Odśwież sesje</p>
      </div>
      <Separator />
      <Button size="lg" className="w-max" onClick={() => refreshSession()}>
        Odśwież
      </Button>
    </div>
  );
}
