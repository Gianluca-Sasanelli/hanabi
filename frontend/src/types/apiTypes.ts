import { NextResponse } from 'next/server'
export type Result<T, E = Error> =
  | { success: true; data: T; status?: number }
  | { success: false; error: E; status?: number }
export interface RawBackendResponse<T = unknown> {
  response: Response
  data: T
  error: Error | null
}

export interface ApiError {
  code: string
  message: string
  details: unknown
}

export interface ApiMeta {
  timestamp: string
  request_id: string
  user_id: string
}

export interface ApiResponse<T> {
  success: boolean
  data: T
  error: ApiError | null
  meta: ApiMeta
}

export function success<T>(data: T, status?: number): Result<T> {
  return { success: true, data, status }
}

export function failure<E = Error>(
  error: E,
  status?: number
): Result<never, E> {
  return { success: false, error, status }
}

export function createBackendError(
  message: string,
  code: string = 'NETWORK_ERROR',
  status: number = 500,
  nextResponse: boolean = false
): Error | NextResponse {
  const error = {
    code,
    message,
  }

  if (nextResponse) {
    return NextResponse.json(
      {
        error,
        success: false,
      },
      { status }
    )
  }

  return new Error(JSON.stringify(error))
}
