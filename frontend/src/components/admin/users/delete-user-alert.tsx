import { adminDeleteUserAction } from "@/actions";
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
import { UserOutWithEmail } from "sharkservers-sdk";

interface DeleteUserAlertProps extends UserOutWithEmail {
  isDeleteModalOpen: boolean;
  setIsDeleteModalOpen: (value: boolean) => void;
}

export default function DeleteUserAlert({ ...props }: DeleteUserAlertProps) {
  async function onDeleteButtonClick() {
    const response = await adminDeleteUserAction({ id: props.id });
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
        description: "Pomyslnie usunięto użytkownika",
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
            Czy napewno chcesz usunąc użytkownika {props.username} ({props.id})?
          </AlertDialogTitle>
          <AlertDialogDescription>
            Ta akcja jest nieodwracalna. Spowoduje trwałe usunięcie konta{" "}
            {props.username} ({props.id}) z bazy danych.
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
