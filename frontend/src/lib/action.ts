import { getServerSession } from "next-auth/next";
import { createSafeActionClient } from "next-safe-action";
import { ApiError } from "sharkservers-sdk";
import { sharkApi } from "./server-api";

export const action = createSafeActionClient({
    handleReturnedServerError(e) {
        // In this case, we can use the 'MyCustomError` class to unmask errors
        // and return them with their actual messages to the client.
        if (e instanceof ApiError) {
            return {
                serverError: e.message,
            };
        }

        // Every other error will be masked with this message.
        return {
            serverError: "Oh no, something went wrong!",
        };
    }
});

export const authAction = createSafeActionClient({
    // Can also be a non async function.
    async middleware() {
        const api = await sharkApi()
        const session = await getServerSession();

        if (!session) {
            throw new Error("Session not found!");
        }

        return {session: session, api: api};
    },
    handleReturnedServerError(e) {
        // In this case, we can use the 'MyCustomError` class to unmask errors
        // and return them with their actual messages to the client.
        if (e instanceof ApiError) {
            return {
                serverError: e.message,
            };
        }

        // Every other error will be masked with this message.
        return {
            serverError: "Oh no, something went wrong!",
        };
    }
});