import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/appshell/HeaderMegaMenu/HeaderMegaMenu";
import { updateActivePage } from "@/stores/LocalStoreActions";
import { Box, Button, Center, Container, Flex, Group, ScrollArea, Stack, Textarea, rem, Text } from "@mantine/core";
import { useEffect, useState } from "react";
import { useRouter } from 'next/router';
import { LeftNavbarMenu } from "@/components/agent/LeftNavbarMenu/LeftNavbarMenu";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import MessagesDisplay from "@/components/agent/MessagesDisplay/MessagesDisplay";
import AgentFrame from "@/components/agent/AgentFrame";

export default function Agent() {
    return <AgentFrame></AgentFrame>
}