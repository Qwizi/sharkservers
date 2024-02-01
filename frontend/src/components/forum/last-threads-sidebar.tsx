import router from "next/router";
import { Button } from "../ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import { Page_ThreadOut_ } from "sharkservers-sdk";
import Thread from "./thread";
import LastThread from "./last-thread";

export default function LastThreadSidebar({...props}: Page_ThreadOut_) {
    const {items} = props;
    return (
        <Card className="mt-10 hidden md:block">
            <CardHeader>
                <CardTitle>Ostatnie tematy</CardTitle>
                <CardDescription>5 ostatnich tematów</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
                {items && items.map((thread, i) => 
                    <LastThread key={i} {...thread} />
                )}
            </CardContent>
        </Card>
    )
}