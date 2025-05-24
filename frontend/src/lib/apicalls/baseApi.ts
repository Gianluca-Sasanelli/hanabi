import { NextRequest, NextResponse } from 'next/server'
import {
  ApiResponse,
  RawBackendResponse,
  Result,
  success,
  failure,
  createBackendError,
} from '@/types/apiTypes'

export async function apiRequest<T>(
  endpoint: string,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
    body?: unknown
    isFormData?: boolean
    headers?: Record<string, string>
  } = {}
): Promise<Result<T>> {
  const { method = 'GET', body, isFormData = false, headers = {} } = options

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

  const response = await fetch(endpoint, requestOptions)
  if (!response.ok) {
    if (response.status === 404) {
      return failure(new Error('The resource was not found'), response.status)
    }
    const errorData = await response.json().catch(() => ({}))
    return failure(errorData.error, response.status)
  }

  if (method === 'DELETE') {
    return success(true as unknown as T, response.status)
  }
  const apiResponse = (await response.json()) as ApiResponse<T>
  return success(apiResponse.data, response.status)
}

export async function fetchFromBackend(
  request: NextRequest,
  endpoint: string,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
    requireAuth?: boolean
    isFormData?: boolean
    returnRawResponse?: boolean
    body?: unknown
    language?: string
  } = { requireAuth: true }
): Promise<NextResponse | RawBackendResponse> {
  try {
    const accessToken = request.headers.get('X-Access-Token')
    if (options.requireAuth && !accessToken) {
      return NextResponse.json(
        { error: 'No access token added by the middleware in the server' },
        { status: 401 }
      )
    }

    const headers: Record<string, string> = {}
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`
    }
    if (!options.isFormData) {
      headers['Content-Type'] = 'application/json'
    }
    if (options.language) {
      if (options.language !== 'en' && options.language !== 'es') {
      } else {
        headers['X-User-Language'] = options.language
      }
    }
    const fetchOptions: RequestInit = {
      method: options.method || 'GET',
      headers,
    }

    if (
      fetchOptions.method !== 'GET' &&
      fetchOptions.method !== 'DELETE' &&
      !options.isFormData
    ) {
      const body = await request.json()
      fetchOptions.body = JSON.stringify(body)
    } else if (options.isFormData) {
      const formData = await request.formData()
      fetchOptions.body = formData
    } else if (options.body) {
      fetchOptions.body = JSON.stringify(options.body)
    }
    const BACKEND_API_URL = process.env.NEXT_BACKEND_API_URL
    const response = await fetch(`${BACKEND_API_URL}${endpoint}`, fetchOptions)

    let data: unknown = {}
    try {
      if (response.status !== 404 && response.status !== 204) {
        data = await response.json()
      }
    } catch (error) {
      console.error('Newtork error or backend not reachable')
    }
    if (options.returnRawResponse) {
      return {
        response,
        data,
        error: null,
      } as RawBackendResponse
    }

    if (response.status === 404 || response.status === 204) {
      return new NextResponse(null, { status: response.status })
    }
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    if (
      error instanceof Error &&
      'cause' in error &&
      (error.cause as unknown as { code: string })?.code === 'ECONNREFUSED'
    ) {
      return createBackendError(
        'Backend server is not running or not reachable',
        'BACKEND_UNREACHABLE',
        503,
        true
      ) as NextResponse
    }
    if (options.returnRawResponse) {
      return {
        response: new Response(null, { status: 500 }),
        data: {},
        error: error as Error,
      } as RawBackendResponse
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
