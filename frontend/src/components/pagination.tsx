'use client';
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";

type PaginationType = {
    total: number;
    size?: number;
}

export default function Pagination({total, size}: PaginationType) {
    const searchParams = useSearchParams();
    const current_page = searchParams.get("page") ?? 1
    const limit = size ?? 10
    const pages = Math.ceil(total / Number(limit))
    const pathname = usePathname();
    let url = pathname + "/?" + searchParams.toString();
    url = url.replace(/&?page=\d+/g, "")
    return (
        <nav className="mt-10">
            <ul className="inline-flex -space-x-px h-10">
                {[...Array(pages)].map((e, i) => <li key={i}>
                    <Link className={current_page == (i + 1) ? "flex items-center justify-center px-4 h-10 leading-tight  border  bg-slate-800 border-gray-700 text-gray-400 hover:bg-slate-700 hover:text-white": "flex items-center justify-center px-4 h-10 border hover:bg-slate-900 hover:text-blue-700 border-gray-700 bg-slate-800 text-white"} href={url + `&page=${i + 1}`}>
                        <span aria-current="page" className={current_page == (i + 1) ? "page-numbers current": "page-numbers"}>{i + 1}</span>
                    </Link>

                </li>)} 

            </ul>
        </nav>
    )
}