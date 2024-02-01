'use client';

import { useState } from "react";
import Image from "next/image";

import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { Dialog, Popover } from '@headlessui/react'
import Link from "next/link";
import { useRouter } from "next/navigation";
import { SwitchTheme } from "../theme-switcher";
import useUser from "@/hooks/user";
import UserMenu from "./user-menu";
import { Separator } from "../ui/separator";
import { useVipModal } from "@/hooks/use-vip-modal";
import { Button } from "../ui/button";


const menuLinks = [
    {
        name: "Forum",
        path: "/forum",
    },
    {
        name: "Użytkownicy",
        path: "/users"
    },
    {
        name: "Gracze",
        path: "/players"
    }
]

const authLinks = [
    {
        name: "Zaloguj się",
        path: "/auth/login",
    },
    {
        name: "Zarejestruj się",
        path: "/auth/register"
    }
]

enum MenuTypeEnum {
    NORMAL = "normal",
    AUTH = "auth"
}

interface IMenuType {
    type: MenuTypeEnum
}



const Header = () => {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
    const { status, isVip } = useUser()
    const router = useRouter()
    const vipModal = useVipModal()


    const MenuLinks = ({ type }: IMenuType) => {
        let links

        switch (type) {
            case MenuTypeEnum.NORMAL:
                return menuLinks.map((link, i) =>
                    <Link key={i} href={link.path} className="text-sm leading-6 text-slate-200 block rounded-md px-3 py-2 font-medium hover:bg-slate-800" onClick={(e) => setMobileMenuOpen(!mobileMenuOpen)}>
                        {link.name}
                    </Link>
                )
            case MenuTypeEnum.AUTH:
                return authLinks.map((link, i) =>
                    <Link key={i} href={link.path} className="text-sm leading-6 text-slate-200 block rounded-md px-3 py-2 font-medium hover:bg-slate-800" onClick={(e) => setMobileMenuOpen(!mobileMenuOpen)}>
                        {link.name}
                    </Link>
                )
        }
    }
    return (
        <header className="border-b">
            <nav className="mx-auto flex container items-center justify-between p-6 " aria-label="Global">
                <div className="flex lg:flex-1">
                    <Link href="/" className="-m-1.5 p-1.5">
                        <span className="sr-only">SharkServers.pl</span>
                        <Image className="h-12 w-auto" src={"/images/logo.png"} alt={"sharkserver.pl"} width={300}
                            height={68} priority/>
                    </Link>
                </div>
                <div className="flex lg:hidden">
                    <button
                        type="button"
                        className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
                        onClick={() => setMobileMenuOpen(true)}
                    >
                        <span className="sr-only">Open main menu</span>
                        <Bars3Icon className="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <Popover.Group className="hidden lg:flex lg:gap-x-12">
                    <MenuLinks type={MenuTypeEnum.NORMAL} />
                </Popover.Group>
                <div className="hidden lg:flex lg:flex-1 lg:justify-end gap-x-12">
                    {status == "authenticated" && !isVip && (<Button variant={"vip"} size="sm" className="mr-2" onClick={vipModal.onOpen}>
                        Ulepsz konto
                    </Button>)}
                    {status == "unauthenticated" && <MenuLinks type={MenuTypeEnum.AUTH} />}
                    {status == "authenticated" && (<UserMenu />)}
                    <SwitchTheme />
                </div>
            </nav>
            <Dialog as="div" className="lg:hidden" open={mobileMenuOpen} onClose={setMobileMenuOpen}>
                <div className="fixed inset-0 z-10" />
                <Dialog.Panel
                    className="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-slate-900 px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="-m-1.5 p-1.5">
                            <span className="sr-only">SharkServers.pl</span>
                            <Image className="h-9 w-auto" src={"/images/logo.png"} alt={"Shark servers.pl"} width={300}
                                height={68} />
                        </Link>
                        <button
                            type="button"
                            className="-m-2.5 rounded-md p-2.5 text-gray-700"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            <span className="sr-only">Close menu</span>
                            <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                        </button>
                    </div>
                    <div className="mt-6 flow-root">
                        <div className="-my-6 divide-y divide-gray-500/10">
                            {status == "unauthenticated" && <MenuLinks type={MenuTypeEnum.AUTH} />}
                            {status == "authenticated" && (
                                <>
                                    <MenuLinks type={MenuTypeEnum.NORMAL} />
                                    <Separator/>
                                    <UserMenu />
                                </>

                            )}
                        </div>
                    </div>
                </Dialog.Panel>
            </Dialog>
        </header>
    )
}

export default Header