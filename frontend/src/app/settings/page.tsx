import UsernameForm from "@/components/settings/username-form";
import { Separator } from "@/components/ui/separator";

export default function SettingsUsernamePage() {
    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium">Nazwa użytkownika</h3>
          <p className="text-sm text-muted-foreground">
            Zaaktualizuj swoją nazwe użytkownika
          </p>
        </div>
        
        <UsernameForm />
      </div>
    )
  }