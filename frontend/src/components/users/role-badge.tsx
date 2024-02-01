import { RoleOut } from "sharkservers-sdk";
import { Badge } from "../ui/badge";

export default function RoleBadge({...props}: RoleOut) {
    const {id, name, color} = props
    return (
        <Badge key={id} variant="outline" style={{ color: color }}>{name}</Badge>
    )
}