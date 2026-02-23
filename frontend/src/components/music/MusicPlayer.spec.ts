﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿import { describe, it, expect } from 'vitest'

// 瀵煎叆鎴戜滑瑕佹祴璇曠殑鍑芥暟
function getAudioUrl(url: string | undefined): string {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const rootUrl = baseUrl.replace('/api/v1', '')
  return `${rootUrl}${url}`
}

describe('getAudioUrl', () => {
  it('should return empty string when url is undefined', () => {
    const result = getAudioUrl(undefined)
    expect(result).toBe('')
  })

  it('should return empty string when url is null', () => {
    const result = getAudioUrl(null as any)
    expect(result).toBe('')
  })

  it('should return the same url when it starts with http', () => {
    const url = 'https://example.com/audio.mp3'
    const result = getAudioUrl(url)
    expect(result).toBe(url)
  })

  it('should return the same url when it starts with https', () => {
    const url = 'https://example.com/audio.mp3'
    const result = getAudioUrl(url)
    expect(result).toBe(url)
  })

  it('should prepend base url when url is relative', () => {
    const url = '/music/audio.mp3'
    const result = getAudioUrl(url)
    expect(result).toBe('http://localhost:8000/music/audio.mp3')
  })

  it('should use VITE_API_BASE_URL from env when available', () => {
    // 淇濆瓨鍘熷鐜鍙橀噺
    const originalBaseUrl = import.meta.env.VITE_API_BASE_URL
    
    // 璁剧疆娴嬭瘯鐜鍙橀噺
    import.meta.env.VITE_API_BASE_URL = 'http://test.example.com/api/v1'
    
    const url = '/music/audio.mp3'
    const result = getAudioUrl(url)
    
    // 楠岃瘉缁撴灉
    expect(result).toBe('http://test.example.com/music/audio.mp3')
    
    // 鎭㈠鍘熷鐜鍙橀噺
    import.meta.env.VITE_API_BASE_URL = originalBaseUrl
  })
})
