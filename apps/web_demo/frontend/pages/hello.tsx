import { updateActivePage } from "@/stores/LocalStoreActions";
import { useRouter } from "next/router";
import { useEffect } from "react";

export default function Hello() {
  const router = useRouter();
    useEffect(() => {
        if (router.isReady) {
            updateActivePage("/")
        }
    }, [router.isReady]);
    
  return (
    <p>hello</p>
  );
}
