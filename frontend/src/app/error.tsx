'use client' // Error components must be Client Components

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useEffect } from 'react'

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    useEffect(() => {
        // Log the error to an error reporting service
        console.error(error)
    }, [error])

    return (
        <Card>
            <CardHeader>
                <CardTitle>Coś poszło nie tak!</CardTitle>
            </CardHeader>
            <CardContent>
            <Button
                onClick={
                    // Attempt to recover by trying to re-render the segment
                    () => reset()
                }
            >
                Spróbuj ponownie
            </Button>
            </CardContent>
        </Card>
    )
}