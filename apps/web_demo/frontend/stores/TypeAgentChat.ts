export interface AgentConversation {
    id: string;
    title?: string | undefined;
    messages: Message[];
    orgStructure?: string | undefined;
    model: string | undefined;
}

export interface Message {
    taskID?: string | undefined;
    localID: string;
    remoteID?: string | undefined;
    name?: string | undefined;
    role?: string | undefined;
    content?: string | undefined;
    tokens?: number | undefined;
  }