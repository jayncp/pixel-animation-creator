---
name: pixel-character-animation
description: Generate pixel-character art and animation end to end from text, general artwork, pixel references, or existing projects. Enter at character design, multi-view references, motion research, animation, cleanup, or export; preserve identity and verify actual pixels and playback.
license: MIT
compatibility: Bundled scripts need Python 3.10+ and Pillow 10–12 (requirements.txt); image generation, editors and players are optional and discovered at runtime.
metadata:
  version: "2.3.0"
---

# Pixel Character Animation

Own the full path from a user's idea to reviewed pixel art and animation. Start at the stage their actual assets support, not automatically at the beginning. Work autonomously on reversible artistic decisions, expose concrete defects, repair them, and verify again. A generated image, successful script, or attractive contact sheet is not proof of a finished animation.

## Route from evidence

1. Inspect supplied images, archives, and existing final indices. Read `START_HERE.md` / `project_resume.json` when supplied; resolve paths from their containing directory. Never select a final merely by the largest version number. Preserve original assets and work in a new revision.
2. Establish the requested deliverable and entry point: text, ordinary image, pixel image, accepted views, motion draft, repair, or export. Read [stages-and-entry.md](references/stages-and-entry.md). Reuse valid upstream work; repair only missing or invalid prerequisites. Imported evidence can satisfy a prerequisite without regenerating it.
3. Default **new character/reference canvases to 256 × 256 pixels per view**, unless the user specifies otherwise. For an existing project, preserve its established size unless asked to migrate. This is a working default, not a scientific minimum or a guarantee of detail. Decide animation/FX bounds separately and record them; do not silently shrink the actor to fit a projectile.
4. Keep a compact project record — `START_HERE.md`, `project_resume.json` and a final index — covering source roles, identity, size, palette/style, views and provenance, action intent, each stage's status with its review evidence, final files, and limitations ([resume-or-new.md](references/resume-or-new.md)). Existing projects do not need conversion merely to receive a small repair.
5. Discover actual tools before choosing a route. Read [tool-adapters.md](references/tool-adapters.md) when generation, native editing, skeleton aids, or setup is needed. Prefer built-in image generation when exposed, existing local tools, and project-local configuration. A binary's presence is not proof of its capabilities, authentication, or free usage.

## A. Create a pixel identity and reference views

Read [character-design.md](references/character-design.md) and [pixel-art-spec.md](references/pixel-art-spec.md).

- **Text:** use available image generation to develop a reference from the description, preserving explicit requirements. Do not substitute an unrelated old character. If generation is unavailable, check supported alternatives and permissions; report an actual capability gap rather than claim generation occurred.
- **General artwork:** inspect the source, extract defining features, and reinterpret them as deliberate pixel clusters at the target size. A downsampled painting is only an intermediate.
- **Pixel artwork:** preserve its design/grid/palette; adapt size with intentional re-authoring where necessary, not smoothing or a distorted stretch.
- Lock a master, identity checklist and palette before deriving views. For a full new reference-set request with no angles specified, start with front, three-quarter, side, and back; disclose that choice. Respect requested subsets and existing accepted views. Add other angles only when useful to the scope. Image generation may assist unseen views; refine them back into target-size pixel art. Label inferred and mirrored views, and check asymmetric details rather than automatically mirror them.
- Compare actual views at matched scale for eyes/face, silhouette, hair, costume construction, footwear, accessories, anatomy, ground line, light direction and perspective. Check discrete identity facts — counts of repeated parts, the side of asymmetric parts, presence of small details — in every view; generated guides break them even when the brief states them. Inspect native-size and enlarged pixels on light/dark backgrounds. Clean contours, cluster noise and palette redundancy without removing identity. Finish this gate before relying on the views to animate.

## B. Research and construct the action

For a new or materially redesigned action, read [motion-research.md](references/motion-research.md), then [motion-design.md](references/motion-design.md).

- Search online for relevant motion references, pixel or non-pixel. Inspect the actual accessible images/frames/video, not titles or descriptions alone. Record sources, what was observed, and what will be adapted. Respect private-upload and source-media rights. If references cannot be accessed, mark research incomplete and distinguish an explicitly provisional motion plan.
- Break the reference into support, line of action, pelvis/chest/head, joint trajectories, key events and real-time rhythm. Manual landmarks or a local Blender/IK proxy are legitimate aids; use pose-estimation tools only when actually available and appropriate. Do not claim automatic skeleton extraction or physical validation from a drawn proxy.
- Retarget intent and normalized trajectories to the character's proportions. Preserve limb lengths, reach, planted contact and volume; adjust angles, steps, torso lean and foreshortening instead of copying a realistic skeleton into a stylized body.
- Block the action without decorative detail or FX. A researched camera view, pose or prop placement stays provisional until the accent poses keep the face and held props readable and within reach. Establish readable key poses, support and center-of-mass shifts, anticipation where appropriate, release/accent, extension, recovery and settle. Record event times in milliseconds and deliberate spacing. **No fixed frame-count cap:** author enough poses to convey the action; holds and duplicate exports are not new poses.
- Keep the strong accent fast and secondary motion offset. Add selective true in-betweens where arcs, depth, view transitions or recovery lose information. Keep named appendage roots/branches/tips continuous in consistent coordinates; attached roots alone do not prevent tail teleportation. Draw effects that follow a part (smears, trails, slash marks left in the air) from that part's sampled path, body travel included.

## C. Refine and validate the actual animation

Read [visual-quality-gates.md](references/visual-quality-gates.md). Restore identity details and correct cloth/depth before final pixel cleanup. Review **every authored frame** against its reference/identity sheet, using face/footwear/appendage close-ups where needed. Examine modified regions with neighboring frames, all turns/occlusions, fast arcs, holds and the loop seam. Do not globally blur, erode, or delete all small components.

Watch the final character-only and FX composite at actual encoded 1× timing for several cycles when you can play it; if you only see stills, review every frame, the anchor trajectories and the exact GIF decode, and leave continuous viewing to the user. Check weight, contact, causality, acceleration/deceleration, follow-through and intentional stylization; physics plausibility is a reasoned visual review, not a solver certificate. Record faults by time/frame/region, repair highest-impact faults and replay. Before calling views or an animation a candidate, have a fresh reviewer inspect the actual images (see the gates reference). If playback or an independent reviewer is unavailable, leave that gate pending and label the output a candidate.

Use [portable-cli.md](references/portable-cli.md) for audits, sampled trajectory diagnostics, contact sheets, edge differences, GIF and sprite-sheet export. Run technical checks separately from visual judgments. A passing palette/alpha/connectivity test does not prove naturalness or user acceptance.

## D. Deliver a resumable result

Read [tools-and-delivery.md](references/tools-and-delivery.md). Deliver the requested stage, not an unsolicited full action suite. Save the master/views, PNG frames, timed GIF, sprite sheet + timing JSON, editable native source or explicitly labeled layered fallback, relevant prompts/configuration, source provenance, review/repair evidence and final index. Reopen native files and compare decoded exports by time interval. Preserve character and FX separation, by depth layer where effects sit both behind and in front of the character.

Stop when the scoped work has been actually reviewed and materially found defects repaired or disclosed; missing capabilities or permissions become precise blockers, not invented passes. Archive the project so a new conversation can inspect its state and resume. This skill is portable guidance, not permission to install globally, accept licenses, incur costs, upload private art, log in, or publish.

## Supporting material

- [Resume/legacy project details](references/resume-or-new.md): older companion packs and conservative repair.
- [Research and design lineage](references/research-lineage.md): sourced decisions, adopted patterns, rejected shortcuts and verification limits.
