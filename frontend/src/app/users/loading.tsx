import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
    return (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
            {[...Array(12)].map((e, i) => <div key={e}>
                <Skeleton  className="h-[320px] w-[320px]" />
            </div>)}
        </div>
    )
}