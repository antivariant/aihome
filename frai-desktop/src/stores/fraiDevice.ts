import { defineStore } from 'pinia'

export type TFTResolutionKey = '1.8" 128x160' | '2.2" 240x320'

export interface TFTResolution {
  width: number
  height: number
  label: TFTResolutionKey
}

const resolutionMap: Record<TFTResolutionKey, { width: number; height: number }> = {
  '1.8" 128x160': { width: 128, height: 160 },
  '2.2" 240x320': { width: 240, height: 320 }
}

export const useFraiDeviceStore = defineStore('fraiDevice', {
  state: () => ({
    tftResolution: {
      label: '1.8" 128x160' as TFTResolutionKey,
      width: resolutionMap['1.8" 128x160'].width,
      height: resolutionMap['1.8" 128x160'].height
    }
  }),
  actions: {
    setResolution(label: TFTResolutionKey) {
      const res = resolutionMap[label]
      this.tftResolution.label = label
      this.tftResolution.width = res.width
      this.tftResolution.height = res.height
    }
  }
})
