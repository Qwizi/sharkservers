import { adminDeleteServerAction, adminDeleteUserAction } from "@/actions";
import { toast } from "@/components/ui/use-toast";
import { useState } from "react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { ServerOut, UserOutWithEmail } from "sharkservers-sdk";

interface DeleteServerAlertProps extends ServerOut {
  isDeleteModalOpen: boolean;
  setIsDeleteModalOpen: (value: boolean) => void;
}

export default function DeleteServerAlert({
  ...props
}: DeleteServerAlertProps) {
  async function onDeleteButtonClick() {
    const response = await adminDeleteServerAction({ id: props.id });
    if (response.serverError) {
      toast({
        variant: "destructive",
        title: "Oh nie. Wystapil bład",
        description: response.serverError,
      });
    } else {
      toast({
        variant: "success",
        title: "Sukces!",
        description: "Pomyslnie usunięto server",
      });
    }
  }

  return (
    <AlertDialog
      open={props.isDeleteModalOpen}
      onOpenChange={props.setIsDeleteModalOpen}
    >
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>
            Czy napewno chcesz usunąc serwer {props.name} ({props.id})?
          </AlertDialogTitle>
          <AlertDialogDescription>
            Ta akcja jest nieodwracalna. Spowoduje trwałe usunięcie serwera{" "}
            {props.name} ({props.id}) z bazy danych.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Anuluj</AlertDialogCancel>
          <AlertDialogAction onClick={() => onDeleteButtonClick()}>
            Usuń
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
