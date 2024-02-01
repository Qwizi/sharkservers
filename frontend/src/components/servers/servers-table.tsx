import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"


export default function ServersTable({ data }: any) {
    console.log
    return (
        <Table>
            <TableCaption>Lista serwerów.</TableCaption>
            <TableHeader>
                <TableRow>
                    <TableHead>Nazwa</TableHead>
                    <TableHead>IP</TableHead>
                    <TableHead>Graczy</TableHead>
                    <TableHead>Mapa</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {data && data.map((server, i) =>
                    <TableRow key={i}>
                        <TableCell className="font-medium">{server.name}</TableCell>
                        <TableCell>{server.ip}:{server.port}</TableCell>
                        <TableCell>{server.players}/{server.max_players}</TableCell>
                        <TableCell>{server.map}</TableCell>
                    </TableRow>
                )}

            </TableBody>
        </Table>
    )
}