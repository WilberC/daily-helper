import { createClient, fetchExchange } from '@urql/vue'

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/graphql/'

export const urqlClient = createClient({
    url: apiUrl,
    exchanges: [fetchExchange],
    fetchOptions: () => {
        return {
            credentials: 'include', // Important for session cookies
            headers: {
                'Content-Type': 'application/json',
            },
        }
    },
})
