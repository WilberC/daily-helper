import { gql } from '@urql/vue'

export const LOGIN_MUTATION = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        isActive
        isStaff
        dateJoined
        createdAt
        updatedAt
      }
    }
  }
`

export const REGISTER_MUTATION = gql`
  mutation Register($input: RegisterInput!) {
    register(input: $input) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        isActive
        isStaff
        dateJoined
        createdAt
        updatedAt
      }
    }
  }
`

export const LOGOUT_MUTATION = gql`
  mutation Logout {
    logout {
      success
      message
    }
  }
`

export const ME_QUERY = gql`
  query Me {
    me {
      id
      username
      email
      firstName
      lastName
      isActive
      isStaff
      dateJoined
      createdAt
      updatedAt
    }
  }
`

export const ALL_USERS_QUERY = gql`
  query AllUsers {
    allUsers {
      id
      username
      email
      firstName
      lastName
      isActive
      isStaff
      dateJoined
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_USER_MUTATION = gql`
  mutation UpdateUser($input: UpdateUserInput!) {
    updateUser(input: $input) {
      success
      message
      user {
        id
        username
        email
        firstName
        lastName
        isActive
        isStaff
        dateJoined
        createdAt
        updatedAt
      }
    }
  }
`
