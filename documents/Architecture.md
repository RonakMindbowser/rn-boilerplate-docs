# Architecture Documentation

## Overview
The Template project is built on a modular architecture designed for scalability, type safety, and clear separation of concerns. It follows a hybrid **MVVM (Model-View-ViewModel)** and **MVC** pattern for screens, combined with **Redux Toolkit** for centralized state management.

---

## 🏗️ Core Design Patterns

### 1. Screen Architecture (MVVM/MVC)
Each screen is divided into three distinct files to separate logic from presentation:

- **`[Screen].tsx` (View)**: Contains only the UI components and layout. It receives data and callbacks from the ViewModel.
- **`[Screen].viewmodel.ts` (Controller/ViewModel)**: A custom hook that contains all the business logic, state handling, and API triggers. It abstracts the "how" from the "what".
- **`[Screen].styles.ts` (Style)**: Uses a `useStyles` hook to provide theme-aware styling.

### 2. State Management (Redux Toolkit)
Centralized state is managed in `src/redux`. 
- **Slices**: Functional areas have their own slices (e.g., `AppSlice`, `UserSlice`).
- **Async Thunks**: Used for handling side effects like API calls and data persistence.

### 3. Navigation (React Navigation 7)
The app uses a nested navigation hierarchy:
- **RootStackNavigator**: The top-level navigator that handles switching between `Auth` and `Main` stacks based on the `accessToken`.
- **MainStackNavigator**: Contains common app screens and the `HomeTabNavigator`.
- **HomeTabNavigator**: Implementation of the primary bottom tab bar.

---

## 📁 Source Directory Structure

```
src/
├── assets/                 # Static assets (Images, fonts, SVGs)
├── components/             # Reusable, atomic UI components
├── contexts/              # React Context providers (Theme, Auth etc.)
├── hocs/                  # Higher-Order Components for cross-cutting concerns
├── hooks/                 # Custom shared React hooks
├── language/              # I18n translations (i18next)
├── navigators/            # Navigation stacks and route definitions
├── networkConfig/         # API endpoints and HTTP service layer
├── redux/                # Global state (Store, Slices, Thunks)
├── screens/              # Feature-specific screen modules
├── theme/                # Global design tokens (Colors, Typography)
├── types/                # Shared TypeScript interfaces and types
└── utils/                # Helper functions and utilities
```

---

## 🔄 Data Flow

### API Requests
1. **Trigger**: A user action in the View calls a method in the **ViewModel**.
2. **Action**: The ViewModel dispatches an **Async Thunk**.
3. **Execution**: The Thunk uses the **HTTPService** to call an **Endpoint**.
4. **State Update**: Upon completion, the Thunk's action is handled by the **Slice's** `extraReducers`, updating the Redux store.
5. **Re-render**: The View automatically re-renders with the updated state from the store via `useAppSelector`.

### Persistence
The app uses **MMKV** (via `StorageService.ts`) for high-performance key-value storage. Critical data like `accessToken` is persisted and retrieved during the app's boot sequence.

---

## 🛡️ Type Safety
The project leverages TypeScript for end-to-end type safety:
- **Navigation**: Routes and params are typed in `routes.ts`.
- **Redux**: Custom `useAppSelector` and `useAppDispatch` hooks ensure state and action types are strictly enforced.
- **API**: Response and request shapes are defined in `src/types/types.ts`.
