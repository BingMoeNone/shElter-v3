
export interface Station {
  id: number
  name: string
  pathKey: string
  description: string | null
  minLevel: number
  isActive: boolean
  metaData: Record<string, any>
  lines: Line[]
}

export interface Line {
  id: number
  name: string
  color: string
  requiredLevel: number
}

export interface Artist {
  id: number
  name: string
  bio: string | null
  avatarUrl: string | null
}

export interface Album {
  id: number
  title: string
  coverUrl: string | null
  releaseDate: string | null
  description: string | null
  artists: Artist[]
}

export interface Track {
  id: number
  title: string
  fileUrl: string
  duration: number | null
  order: number
  albumId: number | null
  album: Album | null
  artists: Artist[]
}
