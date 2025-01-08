import { jwtDecode } from 'jwt-decode'

export interface CustomJwtPayload {
    created_at: string
    description: string
    folder_id: string
    id: number
    name: string
    school_id: number
}
// giai ma token
export const decodeToken = (token: string) => {
    try {
        const infor = jwtDecode<CustomJwtPayload>(token)
        return infor
    } catch (error) {
        return null
    }
}
