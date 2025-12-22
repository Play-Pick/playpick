<template>
  <div class="profile-section">
    <div class="profile-header">
      <div class="profile-image-wrapper">
        <img
          v-if="profileImage"
          :src="profileImage"
          alt="프로필 이미지"
          class="profile-image"
        />
        <div v-else class="profile-image-placeholder">
          <i class="fas fa-user"></i>
        </div>
        <button @click="$emit('toggle-edit')" class="edit-profile-btn">
          <i class="fas fa-camera"></i>
        </button>
      </div>

      <div class="profile-info">
        <div v-if="!isEditMode">
          <h1>{{ user.nickname || user.username }}</h1>
          <p class="username">@{{ user.username }}</p>
          <div class="profile-actions">
            <button @click="$emit('toggle-edit')" class="btn-edit">
              <i class="fas fa-edit"></i> 프로필 수정
            </button>
            <button @click="$emit('show-edit-account')" class="btn-edit-account">
              <i class="fas fa-user-edit"></i> 회원정보 수정
            </button>
          </div>
        </div>

        <div v-else class="edit-form">
          <input
            :value="editForm.nickname"
            @input="$emit('update:editForm', { ...editForm, nickname: $event.target.value })"
            type="text"
            placeholder="닉네임"
            class="input-nickname"
          />
          <div class="image-upload">
            <input
              type="file"
              ref="imageInput"
              @change="handleImageChange"
              accept="image/*"
              class="file-input"
            />
            <button @click="$refs.imageInput.click()" class="btn-upload">
              <i class="fas fa-upload"></i> 이미지 선택
            </button>
          </div>
          <div class="edit-actions">
            <button @click="$emit('save')" class="btn-save">
              <i class="fas fa-check"></i> 저장
            </button>
            <button @click="$emit('cancel-edit')" class="btn-cancel">
              <i class="fas fa-times"></i> 취소
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="stats">
      <div class="stat-item">
        <i class="fas fa-comment"></i>
        <span class="stat-value">{{ articlesCount }}</span>
        <span class="stat-label">작성한 리뷰</span>
      </div>
      <div class="stat-item">
        <i class="fas fa-star"></i>
        <span class="stat-value">{{ averageRating }}</span>
        <span class="stat-label">평균 별점</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  profileImage: {
    type: String,
    default: ''
  },
  isEditMode: {
    type: Boolean,
    default: false
  },
  editForm: {
    type: Object,
    required: true
  },
  articlesCount: {
    type: Number,
    default: 0
  },
  averageRating: {
    type: String,
    default: '0.0'
  }
})

const emit = defineEmits([
  'toggle-edit',
  'show-edit-account',
  'update:editForm',
  'save',
  'cancel-edit',
  'image-change'
])

const imageInput = ref(null)

const handleImageChange = (event) => {
  emit('image-change', event)
}
</script>

<style scoped>
.profile-section {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  transition: background 0.3s, box-shadow 0.3s;
}

:root.dark .profile-section {
  background: #2c2c2c;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
}

.profile-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: center;
}

.profile-image-wrapper {
  position: relative;
}

.profile-image,
.profile-image-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  transition: all 0.3s;
}

.profile-image-placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
}

:root.dark .profile-image-placeholder {
  background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
}

.edit-profile-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  border: 3px solid white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

:root.dark .edit-profile-btn {
  background: #818cf8;
  border-color: #2c2c2c;
}

.edit-profile-btn:hover {
  background: #4f46e5;
  transform: scale(1.1);
}

:root.dark .edit-profile-btn:hover {
  background: #6366f1;
}

.profile-info {
  flex: 1;
}

.profile-info h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

:root.dark .profile-info h1 {
  color: #f3f4f6;
}

.username {
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
  transition: color 0.3s;
}

:root.dark .username {
  color: #9ca3af;
}

.profile-actions {
  display: flex;
  gap: 1rem;
}

.btn-edit,
.btn-edit-account {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-edit {
  background: linear-gradient(to right, #6366f1, #9333ea);
  color: white;
}

:root.dark .btn-edit {
  background: linear-gradient(to right, #818cf8, #a78bfa);
}

.btn-edit:hover {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  transform: scale(1.05);
}

:root.dark .btn-edit:hover {
  background: linear-gradient(to right, #6366f1, #9333ea);
}

.btn-edit-account {
  background: #f3f4f6;
  color: #374151;
}

:root.dark .btn-edit-account {
  background: #374151;
  color: #f3f4f6;
}

.btn-edit-account:hover {
  background: #e5e7eb;
}

:root.dark .btn-edit-account:hover {
  background: #4b5563;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-nickname {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  color: #111827;
}

:root.dark .input-nickname {
  background: #1a1a1a;
  border-color: #374151;
  color: #f3f4f6;
}

.input-nickname:focus {
  outline: none;
  border-color: #6366f1;
}

:root.dark .input-nickname:focus {
  border-color: #818cf8;
}

.image-upload {
  display: flex;
  gap: 1rem;
}

.file-input {
  display: none;
}

.btn-upload {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

:root.dark .btn-upload {
  background: #374151;
  color: #f3f4f6;
}

.btn-upload:hover {
  background: #e5e7eb;
}

:root.dark .btn-upload:hover {
  background: #4b5563;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-save,
.btn-cancel {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-save {
  background: linear-gradient(to right, #10b981, #059669);
  color: white;
}

.btn-save:hover {
  background: linear-gradient(to right, #059669, #047857);
  transform: scale(1.05);
}

.btn-cancel {
  background: #ef4444;
  color: white;
}

.btn-cancel:hover {
  background: #dc2626;
  transform: scale(1.05);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
  transition: border-color 0.3s;
}

:root.dark .stats {
  border-top-color: #374151;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: linear-gradient(135deg, #f9fafb, #ffffff);
  border-radius: 12px;
  transition: all 0.3s;
}

:root.dark .stat-item {
  background: linear-gradient(135deg, #1a1a1a, #2c2c2c);
}

.stat-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.stat-item i {
  font-size: 2rem;
  color: #6366f1;
  margin-bottom: 0.5rem;
  display: block;
  transition: color 0.3s;
}

:root.dark .stat-item i {
  color: #818cf8;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.25rem;
  transition: color 0.3s;
}

:root.dark .stat-value {
  color: #f3f4f6;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.3s;
}

:root.dark .stat-label {
  color: #9ca3af;
}

@media (max-width: 768px) {
  .profile-section {
    padding: 1.5rem;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .profile-actions {
    flex-direction: column;
  }

  .btn-edit,
  .btn-edit-account {
    width: 100%;
    justify-content: center;
  }
}
</style>
