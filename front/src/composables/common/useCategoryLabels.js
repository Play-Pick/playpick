/**
 * 카테고리 라벨 관리 Composable
 */
export const useCategoryLabels = () => {
  const categoryLabels = {
    'REVIEW': '후기',
    'QNA': '질문',
    'FREE': '자유게시판',
    'INFO': '정보공유',
    'EXPECTATION': '기대평'
  }

  const getCategoryLabel = (category) => {
    return categoryLabels[category] || category
  }

  const getCategoryColor = (category) => {
    const colors = {
      'REVIEW': '#3498db',
      'QNA': '#e74c3c',
      'FREE': '#2ecc71',
      'INFO': '#f39c12',
      'EXPECTATION': '#9333ea'
    }
    return colors[category] || '#95a5a6'
  }

  return {
    categoryLabels,
    getCategoryLabel,
    getCategoryColor
  }
}
