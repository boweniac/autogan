export interface AgentConversation {
    id: string;
    title?: string | undefined;
    orgStructure?: string | undefined;
    model: string | undefined;
}

export interface AgentConversationMessage {
    id: string;
    messages: Message[];
}

export interface Message {
    task_id?: string | undefined;
    localID?: string | undefined;
    msg_id?: string | undefined;
    agent_name?: string | undefined;
    message_blocks: MessageBlock[];
}

export interface MessageBlock {
    taskId?: string | undefined;
    localID?: string | undefined;
    msgId?: string | undefined;
    agentName?: string | undefined;
    contentType?: string | undefined;
    contentTag?: string | undefined;
    content?: string | undefined;
    tokens?: number | undefined;
    add_document_progress?: number | undefined;
    text_to_vectors_progress?: number | undefined;
}

// export interface MessageBlock {
//     task_id?: string | undefined;
//     localID?: string | undefined;
//     msg_id?: string | undefined;
//     agent_name?: string | undefined;
//     content_type?: string | undefined;
//     content_tag?: string | undefined;
//     content?: string | undefined;
//     tokens?: number | undefined;
//     add_document_progress?: number | undefined;
//     text_to_vectors_progress?: number | undefined;
// }