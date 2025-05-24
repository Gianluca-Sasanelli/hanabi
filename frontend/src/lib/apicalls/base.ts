import { Result, ApiError } from '@/types/api'

export function success<T>(data: T, status: number): Result<T> {
  return {
    success: true,
    data,
    status
  }
}

export function failure(error: Error | ApiError, status: number): Result<never> {
  return {
    success: false,
    error,
    status
  }
}





export async function apiRequest<T>(
  endpoint: string,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
    body?: unknown
    isFormData?: boolean
    headers?: Record<string, string>
  } = {}
): Promise<Result<T>> {
  const { 
    method = 'GET', 
    body, 
    isFormData = false, 
    headers = {}
  } = options

  const requestOptions: RequestInit = {
    method,
    headers: {
      ...(!isFormData && { 'Content-Type': 'application/json' }),
      ...headers,
    },
  }

  if (body && method !== 'GET' && method !== 'DELETE') {
    if (isFormData) {
      requestOptions.body = body as FormData
    } else {
      requestOptions.body = JSON.stringify(body)
    }
  }

  try {
    const response = await fetch(endpoint, requestOptions)
    if (!response.ok) {
      if (response.status === 404) {
        return failure(new Error('The resource was not found'), response.status)
      }
      const errorData = await response.json().catch(() => ({}))
      return failure(errorData.error || new Error('Request failed'), response.status)
    }

    if (method === 'DELETE') {
      return success(true as unknown as T, response.status)
    }
    if (response.status === 204) {
      return success(null as T, response.status)
    }

    const jsonResponse = await response.json()
    console.log('Raw API Response:', jsonResponse)  // Debug log
    
    return success(jsonResponse.data as T, response.status)
  } catch (error) {
    console.error('API Request failed:', error)
    return failure(error instanceof Error ? error : new Error('Unknown error occurred'), 500)
  }
} 