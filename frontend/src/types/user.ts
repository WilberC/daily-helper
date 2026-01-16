export interface User {
  id: string
  username: string
  email: string
  firstName: string
  lastName: string
  isActive: boolean
  isStaff: boolean
  isSuperuser: boolean
  dateJoined: string
  createdAt: string
  updatedAt: string
}

export interface LoginInput {
  username: string
  password: string
}

export interface RegisterInput {
  username: string
  email: string
  password: string
  firstName?: string
  lastName?: string
  isStaff?: boolean
  isSuperuser?: boolean
  isActive?: boolean
}

export interface LoginPayload {
  success: boolean
  message: string
  user?: User
}

export interface RegisterPayload {
  success: boolean
  message: string
  user?: User
}

export interface LogoutPayload {
  success: boolean
  message: string
}

export interface UpdateUserInput {
  userId: string
  email?: string
  firstName?: string
  lastName?: string
  isStaff?: boolean
  isSuperuser?: boolean
  isActive?: boolean
}

export interface UpdateUserPayload {
  success: boolean
  message: string
  user?: User
}
