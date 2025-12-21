<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { onMounted, computed, ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useThemeStore } from '@/stores/themeStore'
import FloatingActionButtons from '@/components/Common/FloatingActionButtons.vue'
import logoLight from '@/assets/images/logo-light.png'
import logoDark from '@/assets/images/logo-dark.png'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const isMenuOpen = ref(false)

// 현재 테마에 맞는 로고 선택
const currentLogo = computed(() => {
  return themeStore.isDarkMode ? logoDark : logoLight
})

// 앱 초기화 시 인증 상태 확인
onMounted(async () => {
  await authStore.initialize()
  themeStore.initialize()
})

const handleLogout = async () => {
  await authStore.logout()
  isMenuOpen.value = false
  router.push('/login')
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/" class="nav-logo" @click="closeMenu">
          <img :src="currentLogo" alt="공연 커뮤니티 로고" class="logo-image" />
        </RouterLink>
        <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen" aria-label="메뉴 열기/닫기">
          <i class="fas" :class="isMenuOpen ? 'fa-times' : 'fa-bars'"></i>
        </button>
        <div class="nav-menu" :class="{ open: isMenuOpen }">
          <RouterLink to="/" class="nav-link" @click="closeMenu">홈</RouterLink>
          <RouterLink to="/performances" class="nav-link" @click="closeMenu">공연</RouterLink>
          <RouterLink to="/rankings" class="nav-link" @click="closeMenu">랭킹</RouterLink>
          <RouterLink to="/community" class="nav-link" @click="closeMenu">커뮤니티</RouterLink>

          <!-- 인증 상태에 따른 버튼 -->
          <div class="auth-buttons">
            <template v-if="authStore.isAuthenticated">
              <RouterLink to="/mypage" class="nav-link mypage-link" @click="closeMenu">
                <i class="fas fa-user-circle"></i>
                마이페이지
              </RouterLink>
              <span class="username">{{ authStore.username }}</span>
              <button @click="handleLogout" class="nav-btn">로그아웃</button>
            </template>
            <template v-else>
              <RouterLink to="/login" class="nav-btn" @click="closeMenu">로그인</RouterLink>
              <RouterLink to="/register" class="nav-btn btn-register" @click="closeMenu">회원가입</RouterLink>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>

    <footer class="footer">
      <p>&copy; 2025 공연 추천 커뮤니티</p>
    </footer>

    <!-- Floating Action Buttons -->
    <FloatingActionButtons />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  background-color: #ffffff;
  transition: background-color 0.3s;
}

:root.dark body {
  background-color: #1a1a1a;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #ffffff;
  color: #111827;
  padding: 1rem 0;
  transition: background-color 0.3s, color 0.3s;
}

:root.dark .navbar {
  background-color: #1a1a1a;
  color: #f3f4f6;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: inherit;
  cursor: pointer;
}

.nav-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  transition: opacity 0.3s;
}

.nav-logo:hover {
  opacity: 0.8;
}

.logo-image {
  height: 45px;
  width: auto;
  object-fit: contain;
  transition: transform 0.3s;
}

.logo-image:hover {
  transform: scale(1.05);
}

.nav-menu {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #111827;
  text-decoration: none;
  transition: color 0.3s;
}

:root.dark .nav-link {
  color: #f3f4f6;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #6366f1;
}

:root.dark .nav-link:hover,
:root.dark .nav-link.router-link-active {
  color: #818cf8;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-left: 1rem;
}

.username {
  color: #6366f1;
  font-weight: 500;
  transition: color 0.3s;
}

:root.dark .username {
  color: #818cf8;
}

.nav-btn {
  padding: 0.5rem 1rem;
  background-color: transparent;
  color: #111827;
  border: 1px solid #111827;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
}

:root.dark .nav-btn {
  color: #f3f4f6;
  border-color: #f3f4f6;
}

.nav-btn:hover {
  background-color: #111827;
  color: #ffffff;
}

:root.dark .nav-btn:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.btn-register {
  background-color: #6366f1;
  border-color: #6366f1;
  color: white;
}

:root.dark .btn-register {
  background-color: #818cf8;
  border-color: #818cf8;
}

.btn-register:hover {
  background-color: #4f46e5;
  border-color: #4f46e5;
  color: white;
}

:root.dark .btn-register:hover {
  background-color: #6366f1;
  border-color: #6366f1;
  color: white;
}

.mypage-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  transition: all 0.3s;
}

.mypage-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
}

.mypage-link i {
  font-size: 1.2rem;
}

.main-content {
  flex: 1;
  width: 100%;
}

.footer {
  background-color: #f3f4f6;
  color: #111827;
  text-align: center;
  padding: 1rem 0;
  margin-top: 2rem;
  transition: background-color 0.3s, color 0.3s;
}

:root.dark .footer {
  background-color: #1a1a1a;
  color: #f3f4f6;
}

/* Responsive: Offcanvas nav */
@media (max-width: 900px) {
  .nav-container {
    padding: 0 1rem;
  }

  .menu-toggle {
    display: block;
  }

  .nav-menu {
    position: fixed;
    inset: 0;
    top: 64px;
    background: rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(6px);
    display: none;
    flex-direction: column;
    padding: 1rem;
    z-index: 50;
    gap: 0.75rem;
  }

  .nav-menu.open {
    display: flex;
  }

  .nav-menu > .nav-link,
  .nav-menu > .auth-buttons {
    background: #ffffff;
    color: #111827;
    width: 100%;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  :root.dark .nav-menu > .nav-link,
  :root.dark .nav-menu > .auth-buttons {
    background: #1f2937;
    color: #f3f4f6;
  }

  .nav-menu > .nav-link {
    text-align: center;
  }

  .auth-buttons {
    flex-direction: column;
    gap: 0.75rem;
    margin-left: 0;
  }

  .nav-logo img {
    height: 40px;
  }
}
</style>
