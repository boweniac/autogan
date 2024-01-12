export interface AgentConversation {
    id: string;
    title?: string | undefined;
    messages: Message[];
    orgStructure?: string | undefined;
    model: string | undefined;
}

export interface Message {
    task_id?: string | undefined;
    localID?: string | undefined;
    id?: string | undefined;
    agent_name?: string | undefined;
    role?: string | undefined;
    content?: string | undefined;
    tokens?: number | undefined;
  }