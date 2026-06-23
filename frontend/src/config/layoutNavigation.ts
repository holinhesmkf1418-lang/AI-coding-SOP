import type { RouteLocationRaw } from 'vue-router'

export interface LayoutNavigationItem {
  key: string
  label: string
  to: RouteLocationRaw
}

export const layoutNavigationItems: LayoutNavigationItem[] = [
  {
    key: 'home',
    label: '项目列表',
    to: { name: 'home' },
  },
  {
    key: 'settings',
    label: '设置',
    to: { name: 'settings' },
  },
]
