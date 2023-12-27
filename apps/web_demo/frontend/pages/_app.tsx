import { AppProps } from "next/app";
import {AppShell, createTheme, MantineProvider, rem} from '@mantine/core';
import '@mantine/core/styles.css';
import CustHeader from "@/components/appshell/CustHeader";
import {NavbarMinimal} from "@/components/appshell/NavbarMinimal/NavbarMinimal";
import { BottomNavbar } from "@/components/appshell/BottomNavbar/BottomNavbar";
import {LocalState, localStore} from "@/stores/LocalStore";

export default function App({ Component, pageProps }: AppProps) {
    const appName = localStore((state: LocalState) => state.appName);
    const activePage = localStore((state: LocalState) => state.activePage);

    const loginFrameworkPagesList = ["login", "signup"]

    if (loginFrameworkPagesList.includes(activePage)) {
        return <p>login</p>
    } else {
        return (
            <MantineProvider>
                <CustHeader appName={appName}></CustHeader>
                <AppShell
                    navbar={{
                            width: rem(50),
                            breakpoint: 'sm',
                            collapsed: { mobile: true },
                        }}
                >
                    <AppShell.Navbar><NavbarMinimal/></AppShell.Navbar>
                    <AppShell.Main><Component {...pageProps} /></AppShell.Main>
                    <AppShell.Footer><BottomNavbar /></AppShell.Footer>
                </AppShell>
            </MantineProvider>
        )
    }
}