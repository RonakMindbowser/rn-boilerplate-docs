# Assets Documentation

## Overview
This document explains how to manage and utilize static assets (Images, SVGs, and Fonts) within the Template codebase.

---

## Directory Structure
All static assets are located in `src/assets`:

```
src/assets/
├── fonts/          # Custom TTF/OTF font files
├── back.png        # Back icon asset
├── logo.png        # Application logo
└── logosvg.svg     # Vector logo asset
```

---

## 1. Images (PNG, JPG)
Raster images are managed through a centralized utility to ensure consistency and easier refactoring.

### **How to Add a New Image**
1. Place the image file in `src/assets/`.
2. Register the image in `src/utils/ImageConstants.ts`:

```typescript
// src/utils/ImageConstants.ts
const ImageConstants = {
  // ... existing constants
  LogoPng: require('../assets/logo.png'),
  BackIcon: require('../assets/back.png'),
};
```

### **Usage in Components**
```tsx
import { Image } from 'react-native';
import ImageConstants from 'utils/ImageConstants';

const MyComponent = () => (
  <Image source={ImageConstants.LogoPng} style={{ width: 100, height: 100 }} />
);
```

---

## 2. SVGs
We use `react-native-svg` and `react-native-svg-transformer` to import SVGs directly as React components.

### **How to Add a New SVG**
1. Place the `.svg` file in `src/assets/`.
2. Import it directly in your component or screen:

```tsx
import LogoSvg from 'assets/logosvg.svg';

const MyComponent = () => (
  <LogoSvg width={120} height={40} />
);
```

---

## 3. Typography & Fonts
Custom fonts (Poppins) are linked to the project and accessed via typography utilities.

### **Font Configuration**
Fonts are managed in `src/utils/FontUtils.ts`, which maps font weights to Poppins family names.

### **Usage via Typography Utility**
Always use the `getTypographyStyle` helper from `src/utils/Typography.ts` instead of hardcoding `fontFamily`.

```tsx
import { Text } from 'react-native';
import { getTypographyStyle, TypographyStyleEnum } from 'utils/Typography';

const MyComponent = () => (
  <Text style={getTypographyStyle(TypographyStyleEnum.HEADING)}>
    Hello World
  </Text>
);
```

### **Manual Usage**
If you need specific font weights without predefined typography styles:

```tsx
import { Text } from 'react-native';
import { fontFamily } from 'utils/FontUtils';

const MyComponent = () => (
  <Text style={{ fontFamily: fontFamily.bold, fontSize: 16 }}>
    Bold Text
  </Text>
);
```
