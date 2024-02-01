'use client'
import { CategoryOut, Page_CategoryOut_ } from "sharkservers-sdk";
import { Button } from "../ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card";
import { useRouter, useSearchParams } from "next/navigation";

export default function CategoriesSidebar({ ...props }: Page_CategoryOut_) {
    const router = useRouter()
    const searchParams = useSearchParams()

    const categoryId = searchParams.get("category") || undefined

    const { items, total } = props
    return (
        <Card className="mt-10">
            <CardHeader>
                <CardTitle>Kategorie</CardTitle>
                <CardDescription>Wybierz kategorie</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 gap-5">
                {items && items.map((category, i) =>
                    <Button
                        variant="outline"
                        className={category.id == categoryId ? "w-full bg-primary": "w-full"}
                        key={i}
                        onClick={(e) => router.push(`/forum/?category=${category.id}`)}
                    >
                        {category.name} | ({category.threads_count})
                    </Button>
                )}
            </CardContent>
        </Card>
    )
}