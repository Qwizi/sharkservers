
import './globals.css'
import '@uiw/react-markdown-editor/markdown-editor.css';


import type { Metadata } from 'next'
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";
import { ThemeProvider } from "@/components/theme-provider"
import ToasterClient from '@/components/toaster';
import { NextAuthProvider } from '@/components/session-provider';
import { ModalProvider } from '@/components/model-provider';

export const metadata: Metadata = {
    title: 'SharkServers.pl',
    description: 'Sieć serwerów do gry Team Fortress 2',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en" className="bg-background dark">
            <body>
                <ThemeProvider attribute="class" defaultTheme="dark">
                    <NextAuthProvider>
                        <Header />

                        <main className="container mx-auto py-6 sm:px-6 lg:px-8 flex flex-col">
                            <ModalProvider />
                            {children}
                        </main>
                        <ToasterClient />
                        <Footer />
                    </NextAuthProvider>
                </ThemeProvider>
            </body>
        </html>
    )
}
