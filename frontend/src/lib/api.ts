import { authOptions } from "@/app/api/auth/[...nextauth]/route"
import { Session, getServerSession } from "next-auth"
import {ApiClient, SharkServersClient} from "sharkservers-sdk"
export async function authApi(client: any): Promise<ApiClient> {
    const session: Session | null | undefined = await getServerSession(authOptions)
    client.request.config.TOKEN = undefined
    if (session && session?.access_token) {
        client.request.config.TOKEN = session?.access_token.token
    }
    return client
}

SharkServersClient.request.config.BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:80"


const SharkApi = SharkServersClient

export default SharkApi

