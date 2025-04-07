/** LOGIN */
export type LoginRequest = {
    email: string
    password: string
}

export type LoginResponse = {
    refreshToken: string
    access_token: string
}

/** REFRESH TOKEN */

export type RefreshTokenRequest = {
    refreshToken: string
}

export type RefreshTokenResponse = {
    access_token: string
}

/** REGISTER */

export type RegisterRequest = {
    email: string
    name: string
    password: string
}

export type RegisterResponse = {
    //
}

/** I AM ADMIN */

export type IAmAdminResponse = {
    isAdmin: boolean
}
