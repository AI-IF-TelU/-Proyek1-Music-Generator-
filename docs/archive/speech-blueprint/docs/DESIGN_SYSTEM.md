> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# Design System — proposal, Stage 2 gated

## Design principle
Demo-first audio workspace, not a generic SaaS landing page. Source: user-provided Hackathon Master Prompt's anti-AI-slop principles. No fake testimonials, fake metrics, or decorative dashboard cards.

## Direction (to validate with 5–8 references in Stage 2 AMATI)
- Editorial/technical calm; intentional asymmetric spacing.
- Palette candidate: off-white `#F5F5F0`, ink `#1A1A1A`, deep navy `#1E3A5F`, muted teal `#7C9994`.
- Typography candidate: Space Grotesk for display + IBM Plex Mono for small technical labels; test legibility and licensing.
- Hero copy candidate: `Keep the voice. Lose the noise.` (marketing claim, not evidence).
- First viewport contains real upload/demo affordance, not stock imagery.
- Primary interaction: synced A/B waveform, clear progress, accessible controls.
- Respect `prefers-reduced-motion`; no mandatory Three.js.

## Design research gate
Before implementation: inspect 5–8 real sites from Awwwards/Godly/Httpster/SiteInspire/etc.; record URL, hero, typography, palette, layout, motion, wow; choose 2–3; extract patterns without copying.

## Accessibility
Keyboard navigation, visible focus, contrast check, labels, meaningful status announcements, audio controls with text, mobile responsiveness.

## QA
3-second screenshot test with 3 reviewers is a subjective heuristic, not an objective proof of human authorship. Verify performance and accessibility against actual deployment, not promises.

## Identitas merek sementara
- Product name: **Nirava**
- Tagline: **Keep the voice. Lose the noise.**
- Identitas visual belum final sebelum riset referensi Stage 2.
