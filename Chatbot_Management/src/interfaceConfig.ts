// userConfig.ts
export interface User {
    idUser: number
    username: string
    avatarUrl?: string
    phone: string
    email: string
    birthday: string
    gender: string
    address: string
    password: string
    role: string
    status: string
    createdTime: string
    updatedTime: string
    createdBy: string
    roleID: number | null
    schoolID: number
}

export interface RoleManagement {
    role: Role
    users: User[]
}

export interface Role {
    idRole: number
    roleName: string
    description: string
    createdTime: string
    updatedTime: string
    createdBy: string
    updatedBy: string
}

export interface listPermission {
    id: number
    title: string
    value: string
    roleID: Array<number>
}

export interface Question {
    idQuestion: number
    fullName: string
    question: string
    answer: string
    email: string
    status: string
    sentTime: string
    processedBy: string
    processedTime: string
    chatBotID: number
    chatbotName: string
}

export interface Feedback {
    idFeedback: number
    fullName: string
    email: string
    content: string
    feedbackType: string
    status: string
    createdTime: string
    answeredBy: string
    processedTime: string
    chatBotID: number
    chatbotName: string
}

export interface FoldersFiles {
    idFolder: number
    folderName: string
    description: string
    createdAt: string
    documents: File[]
}

export interface FolderGet {
    idFolder: number
    folderName: string
    description: string
    createdAt: string
    createdBy?: string
}

export interface File {
    idDocument: number
    documentName: string
    documentType: string
    dataType: number
    description: string
    pineconeID: string
    folderId: number
    createdTime: string
    createdBy: string
}

export interface School {
    idSchool: number
    schoolName: string
    schoolCode: string
    description: string
    avatarUrl: string
    dateEstablished: string
    address: string
    email: string
    phone: number
    website: string
    createdTime: string
}

export interface DataChatbot {
    idChatBot: number
    chatBotName: string
    description: string
    folderId?: number
    schoolId?: number
    token: string
    avatarUrl: string
    status?: string
    createdTime?: string
    updatedTime?: string
    createdBy?: string
    updateBy?: string
}

export interface Document {
    idDocument: number
    documentName: string
    documentType: string
    dataType: number
    description: string
    pineconeID: string
    folderId: number
    createdTime: string
    createdBy: string
}

export interface User2 {
    id: string
    avatar: string
    name: string
}
export interface Message {
    id: string
    sender: string
    sentTime: string
    content: string
    threadId?: number
}

export type AsyncState = null | 'loading' | 'error' | 'complete'
