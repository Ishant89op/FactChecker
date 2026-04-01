# Design System Specification: The Tactile Archive

## 1. Overview & Creative North Star
**Creative North Star: "The Curated Earth"**

This design system rejects the clinical coldness of modern SaaS interfaces in favor of a high-end, editorial experience that feels tangible, warm, and intentional. By leveraging the organic weights of Newsreader and a sun-drenched palette, we move away from "software" and toward "storytelling."

The "template" look is avoided through **Intentional Asymmetry**. We break the rigid grid by using oversized margins, overlapping containers, and a typography scale that favors dramatic contrast. This system should feel like a premium independent magazine—airy, sophisticated, and grounded in the physical world.

---

## 2. Colors & Tonal Architecture
The palette is rooted in a soft, sand-based foundation with deep, clay-like accents. 

### The "No-Line" Rule
**Borders are prohibited for sectioning.** To separate content, designers must use background color shifts or white space. For example, a global navigation bar should not have a bottom border; it should sit as a `surface-container-low` block against a `surface` background.

### Surface Hierarchy & Nesting
Treat the interface as physical layers of fine paper. 
- **Base Layer:** `surface` (#fcf9f4)
- **Secondary Sectioning:** `surface-container-low` (#f6f3ee)
- **Interactive/Raised Elements:** `surface-container-lowest` (#ffffff)
- **Deep Insets:** `surface-container-high` (#ebe8e3)

### The Glass & Gradient Rule
To prevent the UI from feeling "flat," use Glassmorphism for floating elements (modals, dropdowns). Apply `surface-tint` (#a53c19) at 5% opacity with a `20px` backdrop blur. 
**Signature CTA Texture:** Use a subtle linear gradient on primary buttons moving from `primary` (#781f00) to `primary_container` (#9a3412) at a 45-degree angle. This adds a "fired clay" depth that a flat hex code cannot achieve.

---

## 3. Typography: Newsreader Editorial
We use **Newsreader** exclusively. Its transitional serif characteristics provide the "soul" of this system.

- **Display (lg/md/sm):** These are your "Brand Moments." Use `display-lg` (3.5rem) with tight tracking (-0.02em) to create an authoritative, editorial presence.
- **Headlines:** Use for section titles. Ensure generous `margin-bottom` (token `8` / 2.75rem) to let the serif breathe.
- **Body (lg/md):** Set at a comfortable `line-height` (1.6) to maintain readability against the warm background.
- **Labels (md/sm):** Use these sparingly for utility. Even at small sizes, the Newsreader serif remains legible and high-end.

---

## 4. Elevation & Depth
Hierarchy is achieved through **Tonal Layering**, not structural lines.

- **The Layering Principle:** Depth is "stacked." Place a `surface-container-lowest` card on a `surface-container-low` section to create a soft, natural lift.
- **Ambient Shadows:** When a float is required (e.g., a floating action button), use a diffused shadow: 
  - `box-shadow: 0 12px 32px rgba(87, 66, 60, 0.08);` 
  - Note: The shadow uses a tint of `on_surface_variant` (#57423c) rather than black.
- **The "Ghost Border" Fallback:** If a border is required for accessibility, use the `outline_variant` (#dec0b7) at **15% opacity**. High-contrast, 100% opaque borders are strictly forbidden.

---

## 5. Components

### Buttons
- **Primary:** Gradient fill (`primary` to `primary-container`), `on-primary` (#ffffff) text. Radius: `DEFAULT` (0.5rem).
- **Secondary:** `surface-container-highest` (#e5e2dd) fill with `primary` (#781f00) text. No border.
- **Tertiary:** Pure text button using `primary` color. Underline only on hover.

### Input Fields
- **Style:** Use a "minimalist tray" approach. No four-sided box. Use a `surface-container-high` background with a 2px bottom-stroke of `outline` (#8b716a) that expands on focus.
- **Typography:** Labels should be `label-md` in `on_surface_variant`.

### Cards & Lists
- **The Divider Ban:** Never use `<hr>` tags or 1px dividers. Use a `spacing-6` (2rem) vertical gap or a subtle shift from `surface` to `surface-container-low`.
- **Image Treatment:** All images should have the `DEFAULT` (0.5rem) corner radius to match the component language.

### Chips
- **Selection Chips:** Use `secondary_fixed` (#ffdbd1) with `on_secondary_fixed` (#360f04) text. This provides a warm, sun-baked highlight that guides the eye without the harshness of a primary color.

---

## 6. Do's and Don'ts

### Do
- **Do** use asymmetric layouts. Align a headline to the left but push the body text 2 columns to the right.
- **Do** use `surface-dim` for footers to create a "grounding" effect at the bottom of the page.
- **Do** leverage the `tertiary` (#004172) blue sparingly for success states or subtle links to provide a "cool" contrast to the warm earth tones.

### Don't
- **Don't** use pure black (#000000). Use `on_background` (#1c1c19) for all text.
- **Don't** use standard "drop shadows." Use the Ambient Shadow spec defined in Section 4.
- **Don't** use "center-align" for long-form editorial content. Keep it left-aligned to maintain the professional, journalistic feel of Newsreader.
- **Don't** use icons with sharp 90-degree corners. All iconography should have a slightly rounded, organic stroke to match the `DEFAULT` (0.5rem) roundness of the system.