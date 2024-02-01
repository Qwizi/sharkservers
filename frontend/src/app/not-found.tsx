'use client' // Error components must be Client Components

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    const router = useRouter()

    return (
        <Card>
            <CardHeader>
                <CardTitle>404 - Nie znaleziono strony</CardTitle>
            </CardHeader>
            <CardContent>
            <Button
                onClick={
                    // Attempt to recover by trying to re-render the segment
                    () => router.push("/")
                }
            >
                Powrót to strony głównej
            </Button>
            </CardContent>
        </Card>
    )
}