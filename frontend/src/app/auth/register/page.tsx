import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { RegisterCard } from "@/components/auth/register-card";
import { getServerSession } from "next-auth/next";
import { redirect } from "next/navigation";


export default async function RegisterPage() {
    const session = await getServerSession(authOptions);
    if (session) {
        redirect("/")
    }
    return (
        <section>
            <RegisterCard />
        </section>
    )
}