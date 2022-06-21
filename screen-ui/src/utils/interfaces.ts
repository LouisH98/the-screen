export interface ScreenStatus {
    slide: string,
    brightness: string,
    auto_rotate: boolean,
    rotation: number
}

export type rotations = {
    up: 0,
    right: 90,
    down: 180,
    left: 270
}