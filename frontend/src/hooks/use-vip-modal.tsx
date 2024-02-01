import {create} from "zustand"

interface useVipModalStore {
    isOpen: boolean;
    onOpen: () => void;
    onClose: () => void;
}

export const useVipModal = create<useVipModalStore>((set) => ({
    isOpen: false,
    onOpen: () => set({isOpen: true}),
    onClose: () => set({isOpen: false}),
}))