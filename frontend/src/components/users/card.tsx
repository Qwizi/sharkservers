'use client'
import * as React from "react"
import Image from "next/image";

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { UserOut } from "sharkservers-sdk";
import Username from "./username";
import { Badge } from "../ui/badge";
import { useRouter } from "next/navigation";
import UserInfo from "./user-info";


export function UserCard({ ...props }: UserOut) {
  const { id, username, display_role, avatar } = props
  const router = useRouter()
  
  return (
    <Card className="">
      <CardHeader className="items-center">
        <UserInfo 
          user={...props}
          avatarClassName="w-28 h-28"
        />
      </CardHeader>
    </Card>
  )
}
