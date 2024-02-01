'use client'
import { Button } from "../ui/button";
import CategoriesSidebar from "./categories-sidebar";
import { Page_CategoryOut_, Page_ThreadOut_ } from "sharkservers-sdk";
import Thread from "./thread";
import { useRouter, useSearchParams } from "next/navigation";
import LastThreadSidebar from "./last-threads-sidebar";

interface IForumContainer {
    categories: Page_CategoryOut_,
    threads: Page_ThreadOut_,
    last_threads: Page_ThreadOut_
}

const ForumContainer = ({ categories, threads, last_threads }: IForumContainer) => {
    const router = useRouter()
    const searchParams = useSearchParams()
    const category = searchParams.get("category") || undefined

    return (
        <div className="lg:flex lg:flex-row flex flex-col w-full h-full mt-5 gap-4">
            <div className="w-full lg:w-8/12 order-2 md:order-1  grid gird-cols-1 gap-2">
                {threads?.total > 0 ? threads.items.map((thread, i) =>
                    <Thread key={i} {...thread} />
                ) : (
                    <h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0">
                        Brak tematów
                    </h2>
                )}
            </div>
            <div className="lg:w-4/12 w-full order-1 md:order-1">
                <Button className="w-full text-white" onClick={(e) => router.push(category ? `/forum/create?category=${category}` : "/forum/create")}>Napisz temat</Button>
                <CategoriesSidebar {...categories} />
                <LastThreadSidebar {...last_threads} />
            </div>
        </div>
    )
}

export default ForumContainer