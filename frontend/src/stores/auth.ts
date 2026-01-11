import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginPayload, RegisterPayload, LogoutPayload, RegisterInput } from '@/types/user'
import { LOGIN_MUTATION, REGISTER_MUTATION, LOGOUT_MUTATION, ME_QUERY } from '@/graphql/auth.graphql'
import { urqlClient } from '@/config/api'

export const useAuthStore = defineStore('auth', () => {
    const currentUser = ref<User | null>(null)
    const isLoading = ref(false)

    // Computed properties
    const isAuthenticated = computed(() => currentUser.value !== null)
    const isAdmin = computed(() => currentUser.value?.isStaff === true)
    const isStaff = computed(() => currentUser.value?.isStaff === true)

    // Login action
    const login = async (username: string, password: string): Promise<LoginPayload> => {
        isLoading.value = true

        try {
            const result = await urqlClient.mutation(LOGIN_MUTATION, { username, password }).toPromise()

            if (result.error) {
                isLoading.value = false
                return {
                    success: false,
                    message: result.error.message || 'Login failed',
                }
            }

            const payload = result.data?.login as LoginPayload

            if (payload.success && payload.user) {
                currentUser.value = payload.user
            }

            isLoading.value = false
            return payload
        } catch (error) {
            isLoading.value = false
            return {
                success: false,
                message: error instanceof Error ? error.message : 'An error occurred',
            }
        }
    }

    // Register action (admin only)
    const register = async (input: RegisterInput): Promise<RegisterPayload> => {
        isLoading.value = true

        try {
            const result = await urqlClient.mutation(REGISTER_MUTATION, { input }).toPromise()

            if (result.error) {
                isLoading.value = false
                return {
                    success: false,
                    message: result.error.message || 'Registration failed',
                }
            }

            const payload = result.data?.register as RegisterPayload
            isLoading.value = false
            return payload
        } catch (error) {
            isLoading.value = false
            return {
                success: false,
                message: error instanceof Error ? error.message : 'An error occurred',
            }
        }
    }

    // Logout action
    const logout = async (): Promise<LogoutPayload> => {
        isLoading.value = true

        try {
            const result = await urqlClient.mutation(LOGOUT_MUTATION, {}).toPromise()

            if (result.error) {
                isLoading.value = false
                return {
                    success: false,
                    message: result.error.message || 'Logout failed',
                }
            }

            const payload = result.data?.logout as LogoutPayload

            if (payload.success) {
                currentUser.value = null
            }

            isLoading.value = false
            return payload
        } catch (error) {
            isLoading.value = false
            return {
                success: false,
                message: error instanceof Error ? error.message : 'An error occurred',
            }
        }
    }

    // Fetch current user
    const fetchCurrentUser = async () => {
        try {
            const result = await urqlClient.query(ME_QUERY, {}).toPromise()

            if (!result.error && result.data?.me) {
                currentUser.value = result.data.me as User
            } else {
                currentUser.value = null
            }
        } catch (error) {
            currentUser.value = null
        }
    }

    return {
        currentUser,
        isLoading,
        isAuthenticated,
        isAdmin,
        isStaff,
        login,
        register,
        logout,
        fetchCurrentUser,
    }
})
