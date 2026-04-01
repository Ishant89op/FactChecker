# Design System Strategy: The Obsidian Archive

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Obsidian Archive."** 

This system is designed to evoke the feeling of a private, high-end digital library—an space where information is curated, not just displayed. We are moving away from the "app-like" density of traditional SaaS products toward a sophisticated, editorial experience. By leveraging the authoritative weight of **Newsreader** against a canvas of warm, obsidian-toned surfaces, we create a high-contrast environment that feels both historic and futuristic.

To break the "template" look, designers must embrace **intentional asymmetry**. Use the generous spacing scale to allow elements to breathe, often pushing primary content off-center to create a dynamic, rhythmic flow. Overlapping elements—such as a display header partially masking a surface-container—should be used to suggest physical depth and "stacked" paper layers.

## 2. Colors & Surface Logic

### The Palette
The color language is rooted in "Near-Black" warmth. We avoid cold, clinical grays in favor of deep charcols (`#0F0F0F` / `#131313`) that carry a faint thermal undertone.

*   **Primary Accent:** The muted terracotta (`primary-container`: `#C2410C`) is used sparingly. It is a "seal of quality," reserved for high-value CTAs, active states, or key editorial markers.
*   **The "No-Line" Rule:** Standard 1px borders are strictly prohibited for sectioning. Structural definition must be achieved through **Background Shifts**. To separate a sidebar from a main feed, use `surface-container-low` against `surface`. To highlight a card, use `surface-container-highest` against `surface-dim`.
*   **Surface Hierarchy:** Treat the UI as an architectural stack.
    *   **Base:** `surface` (#131313)
    *   **Lowered Content:** `surface-container-lowest` (#0E0E0E) for recessed areas like search bars or secondary feeds.
    *   **Elevated Content:** `surface-container-high` (#2A2A2A) for primary interactive cards.
*   **The "Glass & Gradient" Rule:** For floating navigation or modal overlays, use semi-transparent versions of `surface-bright` with a `20px` backdrop-blur. Apply a subtle linear gradient to main CTAs transitioning from `primary` (#FFB59D) to `primary-container` (#C2410C) to give the terracotta a "lit from within" glow.

## 3. Typography
The typography scale is the primary driver of the system's editorial authority.

*   **Editorial Authority (Newsreader):** Used for all `display`, `headline`, and `title-lg` roles. This serif typeface should be tracked slightly tighter (-1% to -2%) in large formats to feel like a premium printed masthead.
*   **The Workhorse (Work Sans):** Used for `body` and `label` roles. This provides a clean, modern counterpoint to the serif headers, ensuring high legibility for functional data.
*   **Hierarchy Note:** Use extreme scale differences. A `display-lg` (3.5rem) header followed immediately by a `body-md` (0.875rem) sub-caption creates the high-fashion contrast required for an "archive" feel.

## 4. Elevation & Depth

### The Layering Principle
Forget shadows as a primary tool. Depth is achieved by "Tonal Layering."
*   **Example:** A `surface-container-low` section houses a `surface-container-highest` card. The contrast in lightness provides the "lift."

### Ambient Shadows
When a physical "float" is required (e.g., a dropdown or floating action button):
*   **Color:** Use a tinted shadow (Shadow Color: `#000000` at 40% opacity).
*   **Spread:** High blur (30px - 60px), zero spread. The goal is an ambient "glow" of darkness rather than a sharp edge.

### The "Ghost Border" Fallback
In rare cases where accessibility requires a container boundary (e.g., input fields), use a **Ghost Border**:
*   Token: `outline-variant` (#59413A) at **20% opacity**.
*   This ensures the line is felt rather than seen, maintaining the "The Obsidian Archive" aesthetic.

## 5. Components

### Buttons
*   **Primary:** High-contrast `on-primary` text on `primary-container` (#C2410C). Shape: `ROUND_EIGHT` (0.5rem).
*   **Tertiary/Editorial:** Newsreader Serif text with a `primary` underline (2px) that expands on hover. No container.

### Input Fields
*   **Style:** Minimalist. No solid backgrounds. Use a `surface-container-lowest` bottom-border only, or a subtle `outline-variant` ghost border.
*   **Focus:** Transition the bottom border to `primary` (#FFB59D).

### Cards & Lists
*   **Constraint:** **Zero Dividers.** Use `spacing-6` (2rem) or `spacing-8` (2.75rem) to create separation between list items.
*   **Interaction:** On hover, a card should shift from `surface-container` to `surface-bright`.

### Chips
*   **Style:** Pill-shaped (`full` roundness). Use `surface-container-highest` with `label-md` (Work Sans). High contrast between the background and text is not necessary; keep it tonal.

### Signature Component: The "Archival Header"
A layout pattern where a `display-md` serif header sits atop a `surface-container-low` full-bleed section, with the text partially overlapping the section boundary to break the grid.

## 6. Do's and Don'ts

### Do:
*   **Do** use asymmetrical margins. A 12-column grid is a suggestion; feel free to leave the first 3 columns empty for "white space as a luxury."
*   **Do** use `Newsreader` for numbers and dates to emphasize the "Archive" feel.
*   **Do** use `surface-container-lowest` for deep backgrounds to make primary text pop.

### Don't:
*   **Don't** use pure white (#FFFFFF). Always use `on-surface` (#E5E2E1) to maintain the muted, warm atmosphere.
*   **Don't** use 1px solid dividers. If you feel you need a line, use more whitespace instead.
*   **Don't** use "vibrant" colors. Even the terracotta should feel like it has been aged or sun-bleached.
*   **Don't** use standard shadows. If the element doesn't feel like it's made of stone, glass, or heavy paper, it doesn't belong in the Archive.