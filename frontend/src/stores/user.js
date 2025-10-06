import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import request from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  // ????
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.user_type === 'admin')
  const isStudent = computed(() => user.value?.user_type === 'student')
  const isEnterprise = computed(() => user.value?.user_type === 'enterprise')

  // ????token?axios header
  const setAuthToken = (accessToken, refreshTokenValue = null) => {
    if (accessToken) {
      request.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
      localStorage.setItem('access_token', accessToken)
      token.value = accessToken

      if (refreshTokenValue) {
        localStorage.setItem('refresh_token', refreshTokenValue)
        refreshToken.value = refreshTokenValue
      }
    } else {
      delete request.defaults.headers.common['Authorization']
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      token.value = null
      refreshToken.value = null
    }
  }

  // ????????
  const errorTranslations = {
    'Invalid phone or password': '????????',
    'User account is disabled': '????????',
    'Must include phone and password': '??????????'
  }

  // ??????
  const translateError = (message) => {
    return errorTranslations[message] || message
  }

  // ??
  const login = async (credentials) => {
    try {
      const response = await request.post('/auth/login/', credentials)
      const { access_token, refresh_token, user: userData } = response.data

      setAuthToken(access_token, refresh_token)
      user.value = userData

      return { success: true, data: response.data }
    } catch (error) {
      console.error('????:', error)
      let errorMessage = error.response?.data?.message ||
                        error.response?.data?.detail ||
                        error.response?.data?.non_field_errors?.[0] ||
                        '????'

      return {
        success: false,
        message: translateError(errorMessage)
      }
    }
  }

  // ??
  const register = async (userData) => {
    try {
      const response = await request.post('/auth/register/', userData)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('????:', error)
      const errorData = error.response?.data
      let message = '????'

      if (errorData) {
        if (typeof errorData === 'string') {
          message = errorData
        } else if (errorData.message) {
          message = errorData.message
        } else if (errorData.phone) {
          message = `???: ${errorData.phone[0]}`
        } else if (errorData.email) {
          message = `??: ${errorData.email[0]}`
        } else if (errorData.password) {
          message = `??: ${errorData.password[0]}`
        }
      }

      return { success: false, message }
    }
  }

  // ??
  const logout = async () => {
    try {
      if (refreshToken.value) {
        await request.post('/auth/logout/', {
          refresh_token: refreshToken.value
        })
      }
    } catch (error) {
      console.error('????:', error)
    } finally {
      setAuthToken(null)
      user.value = null
    }
  }

  // ??????
  const fetchUserInfo = async () => {
    try {
      const response = await request.get('/users/users/profile/')
      user.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('????????:', error)
      return { success: false, message: '????????' }
    }
  }

  // ????
  const updateProfile = async (profileData) => {
    try {
      const response = await request.put('/users/users/update_profile/', profileData)
      user.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('??????:', error)
      return { success: false, message: '??????' }
    }
  }

  // ???token
  if (token.value) {
    setAuthToken(token.value, refreshToken.value)
  }

  return {
    user,
    token,
    refreshToken,
    isLoggedIn,
    isAdmin,
    isStudent,
    isEnterprise,
    login,
    register,
    logout,
    fetchUserInfo,
    updateProfile,
    setAuthToken
  }
})
