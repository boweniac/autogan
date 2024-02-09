import { useEffect, useState } from 'react';
import { useRouter } from "next/router";
import Head from "next/head";
import { rem, useMantineColorScheme } from '@mantine/core';

type CustHeaderProps = {
    appName: string;
}

export default function CustHeader(props: CustHeaderProps) {
    const router = useRouter();
    const { setColorScheme } = useMantineColorScheme();
    const [customize, setCustomize] = useState<string | undefined>();
    let title = "";
    let icon = "";

    useEffect(() => {
        if (router.isReady) {
            setColorScheme('auto')
            setCustomize(router.query.customize as string | undefined);
        }
    }, [router.isReady, router.query.customize]);

    if (router.isReady) {
        switch (true) {
            case customize && customize.includes('xunzhong'):
                title = "讯众";
                icon = "favicon.ico";
                break
            default:
                title = props.appName;
                icon = "favicon.ico";
        }
    }

    return (
        <Head>
            <title>{title}</title>
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1.0"
            />
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
            <meta name="apple-mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-status-bar-style" />
            <link rel="icon" href={`/${icon}`} />
            <link rel="manifest" href="/manifest.json" />
        </Head>
    );
}