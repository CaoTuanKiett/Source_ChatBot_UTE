/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosError, type AxiosRequestConfig, type AxiosResponse } from 'axios'

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const axiosClient = axios.create({
    baseURL: `${VITE_API_URL}/${VITE_API_VERSION}`
})

axiosClient.interceptors.request.use((config) => {
    config.headers['Content-Type'] = 'application/json'
    config.headers['Access-Control-Allow-Origin'] = '*'
    // X-CSRFToken: FGWp2aF83aGv8UNqTUzKom4RwMfsYo5kSqzdHahcsi495vgsyYnzBEgY9OohXcWr

    const access_token = localStorage.getItem('access_token')
    if (access_token) {
        config.headers.Authorization = `Bearer ${access_token}`
    }

    return config
})

axiosClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const resp = error.response as any
        const respErrorCode = resp?.status ?? 500
        if (respErrorCode === 401) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refreshToken')
            window.location.href = '/login'
        }
        const respErrorMessage = resp?.data?.error ?? resp?.data?.message ?? 'UNKNOWN_ERROR'

        throw new Error(respErrorMessage)
    }
)

function $post<T = any, R = AxiosResponse<T>, D = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D>
): Promise<R> {
    try {
        return axiosClient.post<T, R>(url, data, config)
    } catch (error) {
        return Promise.reject(error)
    }
}

function $get<T = any, R = AxiosResponse<T>, D = any>(
    url: string,
    config?: AxiosRequestConfig<D>
): Promise<R> {
    try {
        return axiosClient.get<T, R>(url, config)
    } catch (error) {
        return Promise.reject(error)
    }
}

function $put<T = any, R = AxiosResponse<T>, D = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D>
): Promise<R> {
    try {
        return axiosClient.put<T, R>(url, data, config)
    } catch (error) {
        return Promise.reject(error)
    }
}

function $patch<T = any, R = AxiosResponse<T>, D = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D>
): Promise<R> {
    try {
        return axiosClient.patch<T, R>(url, data, config)
    } catch (error) {
        return Promise.reject(error)
    }
}

function $delete<T = any, R = AxiosResponse<T>, D = any>(
    url: string,
    config?: AxiosRequestConfig<D>
): Promise<R> {
    try {
        return axiosClient.delete<T, R>(url, config)
    } catch (error) {
        return Promise.reject(error)
    }
}

export { $delete, $get, $patch, $post, $put }
