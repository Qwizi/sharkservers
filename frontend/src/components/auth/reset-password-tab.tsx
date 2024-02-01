'use client'
import { Tabs, TabsContent } from "../ui/tabs";
import ConfirmResetPasswordForm from "./confirm-reset-password-form";
import ResetPasswordForm from "./reset-password-form";

interface IResetPasswordTab {
    tab: string
    setTab: Function
    defaultEmail?: string | undefined
    disabledEmailField?: boolean | undefined
}

export default function ResetPasswordTab({tab, setTab, defaultEmail, disabledEmailField}: IResetPasswordTab) {

    const onTabChange = (value) => {
        setTab(value);
    }

    return (
        <Tabs defaultValue={"e-mail"} onValueChange={onTabChange} value={tab}>

            <TabsContent value="e-mail">
                <ResetPasswordForm setTab={setTab} defaultEmail={defaultEmail}
                disabledEmailField={disabledEmailField} />
            </TabsContent>
            <TabsContent value="confirm">
                <ConfirmResetPasswordForm />
            </TabsContent>
        </Tabs>
    )
}