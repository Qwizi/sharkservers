import { Page_UserOut_ } from "sharkservers-sdk";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import Username from "./username";

export default function LastOnlineUsers({ ...props }: Page_UserOut_) {
    const { items, total } = props
    return (
        <Card className="mt-10">
            <CardHeader>
                <CardTitle>
                    Kto jest online ({total})
                </CardTitle>
            </CardHeader>
            <CardContent className="flex">
                {items ? items.map((user, i) =>
                    <div key={i}>
                        <Username
                            
                            user={...user}
                            className="mr-1 after:content-[',']
                            after:text-white
                            "
                        />
                    </div>

                ) : (
                    <p>Brak użytkowników online</p>
                )}
            </CardContent>
        </Card>
    )
}