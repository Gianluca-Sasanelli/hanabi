export interface ApiMeta {
  timestamp: string
}

export interface ApiError {
  code: string
  message: string}

export interface ApiResponse<T> {
  success: boolean
  data: T
  error: ApiError | null
  meta: ApiMeta
}

export interface Result<T> {
  success: boolean
  data?: T
  error?: Error | ApiError
  status: number
} 