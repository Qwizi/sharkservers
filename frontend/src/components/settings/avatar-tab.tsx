'use client'
import { useSession } from "next-auth/react";
import { Separator } from "../ui/separator";
import Image from "next/image"
import AvatarForm from "./avatar-form";
import { Skeleton } from "@/components/ui/skeleton"

export default function AvatarTab() {
    const { data: session, status } = useSession()
    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">Avatar</h3>
                <p className="text-sm text-muted-foreground">
                    Zaaktualizuj avatar
                </p>
            </div>
            <Separator />
            {status == "loading" ? (
                <div className="flex flex-col space-x-4">
                    <Skeleton className="h-24 w-24 rounded-full" />
                    <div className="space-y-2 mt-10">
                        <Skeleton className="h-4" />
                        <Skeleton className="h-4" />
                    </div>
                </div>
            ) : (
                <>
                    <Image src={session?.user?.avatar} width="100" height="100" />
                    <Separator />
                    <AvatarForm />
                </>
            )}

        </div>
    )
}