import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import LoginCard from "@/components/auth/login-card";
import { getServerSession } from "next-auth/next";
import { redirect } from "next/navigation";

export default async function LoginPage() {
    const session = await getServerSession(authOptions);
    if (session) {
        redirect("/")
    }
    return (
        <section>
            <LoginCard/>
        </section>
    )
}