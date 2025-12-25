import { ref } from 'vue'

export function useKakaoMap() {
    const showMapModal = ref(false)
    let map = null
    let geocoder = null

    const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY

    // 카카오 맵 스크립트 로드
    const loadKakaoMapScript = () => {
        return new Promise((resolve, reject) => {
            if (window.kakao && window.kakao.maps) {
                resolve()
                return
            }

            const script = document.createElement('script')
            script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&libraries=services&autoload=false`
            script.async = true
            script.onload = () => {
                if (window.kakao && window.kakao.maps) {
                    window.kakao.maps.load(() => {
                        resolve()
                    })
                } else {
                    reject(new Error('카카오 맵 객체를 찾을 수 없습니다.'))
                }
            }
            script.onerror = (error) => {
                console.error('카카오 맵 스크립트 로드 실패:', error)
                reject(new Error('카카오 맵 API 키를 확인해주세요.'))
            }
            document.head.appendChild(script)
        })
    }

    // 지도 모달 열기
    const openMapModal = async () => {
        showMapModal.value = true

        try {
            await loadKakaoMapScript()
            // 모달이 렌더링된 후 지도 초기화
            setTimeout(() => {
                return true
            }, 100)
        } catch (error) {
            console.error('카카오 맵 로드 실패:', error)
            alert('지도를 불러올 수 없습니다.')
            showMapModal.value = false
        }
    }

    // 지도 모달 닫기
    const closeMapModal = () => {
        showMapModal.value = false
    }

    // 지도 초기화
    const initMap = (venueName) => {
        const mapContainer = document.getElementById('map')
        if (!mapContainer) return

        const mapOption = {
            center: new window.kakao.maps.LatLng(37.5665, 126.978),
            level: 3,
        }

        map = new window.kakao.maps.Map(mapContainer, mapOption)
        geocoder = new window.kakao.maps.services.Geocoder()

        // 주소로 좌표 검색
        geocoder.addressSearch(venueName, (result, status) => {
            if (status === window.kakao.maps.services.Status.OK) {
                const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x)

                const marker = new window.kakao.maps.Marker({
                    map: map,
                    position: coords,
                })

                const infowindow = new window.kakao.maps.InfoWindow({
                    content: `<div style="padding:5px;font-size:12px;">${venueName}</div>`,
                })
                infowindow.open(map, marker)
                map.setCenter(coords)
            } else {
                // 주소 검색 실패 시 키워드 검색
                const ps = new window.kakao.maps.services.Places()
                ps.keywordSearch(venueName, (data, status) => {
                    if (status === window.kakao.maps.services.Status.OK) {
                        const coords = new window.kakao.maps.LatLng(data[0].y, data[0].x)

                        const marker = new window.kakao.maps.Marker({
                            map: map,
                            position: coords,
                        })

                        const infowindow = new window.kakao.maps.InfoWindow({
                            content: `<div style="padding:5px;font-size:12px;">${data[0].place_name}</div>`,
                        })
                        infowindow.open(map, marker)
                        map.setCenter(coords)
                    } else {
                        alert('장소를 찾을 수 없습니다.')
                    }
                })
            }
        })

        map.relayout()
    }

    return {
        showMapModal,
        openMapModal,
        closeMapModal,
        initMap
    }
}
