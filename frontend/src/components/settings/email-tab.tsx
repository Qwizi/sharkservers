
'use client'
import { useState } from "react";
import { Separator } from "../ui/separator";
import EmailForm from "./email-form";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import ConfirmEmailCode from "./confirm-email-form";

export default function EmailTab() {
    const [open, setOpen] = useState(false)
    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">E-mail</h3>
                <p className="text-sm text-muted-foreground">
                    Zaaktualizuj swoj email
                </p>
            </div>
            <Separator />
            <EmailForm setOpen={setOpen}/>
            <Dialog open={open} onOpenChange={setOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Wysłaliśmy wiadomość na twoj nowy podany adres</DialogTitle>
                        <DialogDescription>
                            W treści otrzymałeś kod potrzebny do potwierdzenia zmiany adresu e-mail. Wpisz go do formularza poniżej
                        </DialogDescription>
                    </DialogHeader>
                    <ConfirmEmailCode setOpen={setOpen}/>
                </DialogContent>
            </Dialog>
        </div>
    )
}