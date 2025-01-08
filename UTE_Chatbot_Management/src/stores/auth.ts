/* eslint-disable @typescript-eslint/no-explicit-any */
import { apiLogin, apiRefreshToken } from '@/api'
import { type LoginRequest } from '@/api/auth/auth.dto'
import router, { RoutePath } from '@/router'
import { jwtDecode } from 'jwt-decode'
import { defineStore } from 'pinia'

interface AuthStoreState {
    access_token?: string
    refreshToken?: string
    payload?: {
        exp: number // unix timestamp: 1633835614
        iat: number // unix timestamp: 1633832014
        jti: string // jwt unique identifier: 1e7b7b7b-7b7b-4b7b-8b7b-7b7b7b7b7b7b
        idUser: number
        username: string
        avatarUrl: string
        email: string
        position: string
        roleID: number
        roleName: string
        schoolID: number
        status: string
    }
    returnUrl?: string
    refreshTokenTimeout?: ReturnType<typeof setTimeout>
}

export const useAuthStore = defineStore({
    id: 'auth',
    state: (): AuthStoreState => ({}),
    getters: {
        isLoggedIn(state) {
            return !!state.access_token
        }
    },
    actions: {
        async login(payload: LoginRequest) {
            const loginResp = await apiLogin(payload)
            console.log(':::login -> loginResp', loginResp)

            this.saveAuthData({
                access_token: loginResp.access_token,
                refreshToken: loginResp.refreshToken,
                payload: jwtDecode(loginResp.access_token)
            })

            router.push(this.returnUrl || RoutePath.Home)
        },
        async clear() {
            console.debug('clear')
            this.access_token = undefined
            this.refreshToken = undefined
            this.payload = undefined
            this.returnUrl = undefined
            this.stopRefreshTokenTimer()
            localStorage.removeItem('access_token')
            localStorage.removeItem('refreshToken')
        },
        async logout() {
            // revoke token, stop refresh timer, and clear local storage
            // TODO: Call API to revoke token
            this.clear()
            router.push(RoutePath.Login)
        },
        //
        saveAuthData(data: { access_token: string; refreshToken?: string; payload?: any }) {
            if (data.access_token) {
                this.access_token = data.access_token
                this.startRefreshTokenTimer()
                localStorage.setItem('access_token', data.access_token)
            }
            if (data.refreshToken) {
                this.refreshToken = data.refreshToken
                localStorage.setItem('refreshToken', data.refreshToken)
            }

            if (data.payload) this.payload = data.payload

            this.startRefreshTokenTimer()
        },

        async doPersistAuthData() {
            const access_token = localStorage.getItem('access_token')
            const refreshToken = localStorage.getItem('refreshToken')

            if (!access_token || !refreshToken) {
                this.clear()
                return
            }

            this.saveAuthData({
                access_token,
                refreshToken,
                payload: jwtDecode(access_token)
            })

            await this.doRefreshToken(refreshToken)
        },
        async doRefreshToken(refreshToken?: string) {
            try {
                const _refreshToken = refreshToken ?? this.refreshToken
                if (!_refreshToken) {
                    console.debug('no refresh token')
                    throw new Error()
                }

                const respData = await apiRefreshToken({
                    refreshToken: _refreshToken
                })
                if (!respData?.access_token) {
                    console.debug('no access token in resp')
                    throw new Error()
                }

                this.saveAuthData({
                    access_token: respData.access_token
                })
            } catch (error) {
                console.error('doRefreshToken error', error)
                alert('Session expired. Please login again.')
                this.logout()
            }
        },
        startRefreshTokenTimer() {
            if (!this.payload) {
                return
            }
            const expires = new Date(this.payload.exp * 1000)
            const timeout = expires.getTime() - Date.now() - 60 * 1000
            this.refreshTokenTimeout = setTimeout(this.doRefreshToken, timeout)
        },
        stopRefreshTokenTimer() {
            if (!this.refreshTokenTimeout) {
                return
            }
            clearTimeout(this.refreshTokenTimeout)
        }
    }
})
