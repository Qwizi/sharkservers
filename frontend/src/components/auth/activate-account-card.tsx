'use client'

import { Card, CardHeader, CardTitle, CardContent } from "../ui/card";
import ActivateAccountForm from "./activate-account-form";

export default function ActivateAccountCard() {

    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    Aktywuj konto
                </CardTitle>
            </CardHeader>
            <CardContent>
                <ActivateAccountForm />
            </CardContent>
        </Card>
    )
}