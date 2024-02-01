import NextAuth from "next-auth";
import { UserOut } from "sharkservers-sdk";

declare module "next-auth" {
    interface Session {
        user: UserOut,
        access_token: TokenOut,
        refresh_token: TokenOut
    }
}